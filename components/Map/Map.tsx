/* eslint-disable @typescript-eslint/no-explicit-any */
import styled from 'styled-components'
import DeckGL, { PolygonLayer, RGBAColor } from 'deck.gl'
import React, {
  useEffect, useMemo, useRef, useState,
} from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'
import NextNProgress from 'nextjs-progressbar'
import Link from 'next/link'
import { colorTheme } from '../../Theme'
import { mapColors } from '../shared'
import { deviceSizesPx, onTouchDevice } from '../../utils/devices'
import {
  MapProps, MunicipalityTapInfo, MunicipalityData,
} from '../../utils/types'

const INITIAL_VIEW_STATE = {
  longitude: 17.062927,
  latitude: 63,
  zoom: 3.5,
  minZoom: 3,
  pitch: 0,
  bearing: 0,
}

const TOOLTIP_COMMON_STYLE = {
  backgroundColor: colorTheme.newColors.black3,
  borderRadius: '5px',
  fontSize: '14px',
  color: colorTheme.newColors.white,
}

const TOOLTIP_MOBILE_STYLE = {
  position: 'absolute',
  padding: '0.5em 1em',
  display: 'flex',
  alignItems: 'center',
  ...TOOLTIP_COMMON_STYLE,
} as React.CSSProperties // https://stackoverflow.com/questions/46710747

const DeckGLWrapper = styled.div`
  height: 100%;
`

const hexToRGBA = (hex: string): RGBAColor => {
  const hexValue = hex.replace('#', '')
  const red = parseInt(hexValue.substring(0, 2), 16)
  const green = parseInt(hexValue.substring(2, 4), 16)
  const blue = parseInt(hexValue.substring(4, 6), 16)
  return [red, green, blue]
}

const getColor = (
  dataPoint: number | string | Date,
  boundaries: number[] | string[] | Date[],
): RGBAColor => {
  const colors: RGBAColor[] = mapColors.map(hexToRGBA)

  // Special case for binary KPIs
  if (boundaries.length === 2) {
    return dataPoint === boundaries[0] ? colors[1] : colors[colors.length - 1]
  }

  // Special case for KPIs with three cases
  if (boundaries.length === 3) {
    if (dataPoint > boundaries[1]) {
      return colors[colors.length - 1]
    }
    if (dataPoint > boundaries[0]) {
      return colors[3]
    }
    return colors[1]
  }

  // Special case for invalid dates
  const invalidDate = (possibleDate: unknown) => possibleDate instanceof Date && Number.isNaN(possibleDate.getTime())
  if (invalidDate(dataPoint)) {
    return colors[colors.length - 1]
  }

  const ascending = boundaries[0] < boundaries[1]

  if (ascending) {
    for (let i = boundaries.length - 1; i >= 0; i -= 1) {
      if (dataPoint >= boundaries[i]) {
        return colors[i + 1]
      }
    }
    return colors[0]
  }

  for (let i = 0; i < boundaries.length; i += 1) {
    if (dataPoint >= boundaries[i]) {
      return colors[i]
    }
  }
  return colors[5]
}

// Use when viewState is reimplemented
/* const MAP_RANGE = {
  lon: [8.107180004121693, 26.099158344940808],
  lat: [61.9, 63.9],
} */

export function isMunicipalityData(
  thing: MunicipalityData | unknown,
): thing is MunicipalityData {
  if (!thing) {
    return false
  }
  const mData = thing as MunicipalityData
  return Boolean(
    mData.name && mData.dataPoint && mData.formattedDataPoint && mData.geometry,
  )
}

function MobileTooltip(
  { tInfo, boundaries }: {
    tInfo: MunicipalityTapInfo,
    boundaries: number[] | string[] | Date[]
  },
) {
  return (
    <Link
      href={`/kommun/${tInfo.mData.name.toLowerCase()}`}
      style={{
        ...TOOLTIP_MOBILE_STYLE,
        left: tInfo.x,
        top: tInfo.y,
        textDecoration: 'none',
      }}
    >
      <img
        src="/icons/info.svg"
        alt="info icon"
        style={{
          color: colorTheme.newColors.white, height: 14, width: 14, marginRight: 4,
        }}
      />
      <span style={{ textDecoration: 'underline' }}>
        {`${tInfo.mData.name}`}
        :
      </span>
      <span style={{ color: `rgba(${getColor(tInfo.mData.dataPoint, boundaries)})`, fontWeight: 'bold' }}>
        {`${tInfo.mData.formattedDataPoint}%`}
      </span>
    </Link>
  )
}

function Map({
  data, boundaries, children,
}: MapProps) {
  const [municipalityFeatureCollection, setMunicipalityFeatureCollection] = useState<any>({})
  // "tapped" municipality tooltips are only to be used on touch devices.
  const [lastTapInfo, setLastTapInfo] = useState<MunicipalityTapInfo | null>(null)
  const wrapperRef = useRef<HTMLDivElement | null>(null)

  const router = useRouter()

  const [initialViewState, setInitialViewState] = useState(INITIAL_VIEW_STATE)

  // Update zoom based on window size
  const updateZoom = () => {
    let newZoom = 3.5
    const width = window.innerWidth

    if (width <= deviceSizesPx.tablet) {
      // Tablet or mobile
      newZoom = 3
    }

    setInitialViewState((prevState) => ({
      ...prevState,
      zoom: newZoom,
    }))
  }

  // stop map view from moving away from Sweden
  const enforceMapBounds = ((viewState: any) => ({
    ...viewState,
    longitude: Math.min(24, Math.max(10, viewState.longitude)),
    latitude: Math.min(70, Math.max(55, viewState.latitude)),
  }))

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('/api/map')
      setMunicipalityFeatureCollection(response.data)
    }
    fetchData()
  }, [])

  useEffect(() => {
    window.addEventListener('resize', updateZoom)
    updateZoom() // Initial call to set correct zoom

    // Cleanup
    return () => window.removeEventListener('resize', updateZoom)
  }, [])

  useEffect(() => {
    function clearToolTipOnOutsideTap(ev: TouchEvent) {
      if (wrapperRef.current && ev.target && !wrapperRef.current.contains(ev.target as HTMLElement)) {
        setLastTapInfo(null)
      }
    }
    document.addEventListener('touchstart', clearToolTipOnOutsideTap)
    return () => document.removeEventListener('touchstart', clearToolTipOnOutsideTap)
  }, [wrapperRef])

  const municipalityLines = useMemo(() => municipalityFeatureCollection?.features?.flatMap(
    ({ geometry, properties: { name } }: { geometry: any; properties: { name: string } }) => {
      const currentMunicipality = data.find((e) => e.name === name)
      const dataPoint = currentMunicipality?.primaryDataPoint
      const formattedDataPoint = currentMunicipality?.formattedPrimaryDataPoint

      if (geometry.type === 'MultiPolygon') {
        return geometry.coordinates.map((coords: any) => ({
          geometry: coords[0],
          name,
          dataPoint,
          formattedDataPoint,
        }))
      }
      return [
        {
          geometry: geometry.coordinates[0][0],
          name,
          dataPoint,
          formattedDataPoint,
        },
      ]
    },
  ), [data, municipalityFeatureCollection?.features])

  const municipalityLayer = useMemo(() => new PolygonLayer({
    id: 'polygon-layer',
    data: municipalityLines,
    stroked: true,
    filled: true,
    extruded: false,
    wireframe: false,
    lineWidthUtils: 'pixels',
    lineWidthMinPixels: 0.5,
    getLineWidth: 80,
    lineJointRounded: true,
    getElevation: 0,
    polygonOffset: 1,
    getPolygon: (k: any) => k.geometry,
    getLineColor: () => [0, 0, 0, 80],
    getFillColor: (d) => getColor((d as MunicipalityData).dataPoint, boundaries),
    pickable: true,
  }), [boundaries, municipalityLines])

  return (
    <DeckGLWrapper ref={wrapperRef}>
      <NextNProgress
        color={colorTheme.newColors.blue1}
        startPosition={0.3}
        stopDelayMs={20}
        height={5}
        showOnShallow={false}
        options={{
          showSpinner: false,
        }}
      />
      <DeckGL
        initialViewState={initialViewState}
        controller={{}}
        getTooltip={({ object: mData }) => {
          if (!isMunicipalityData(mData) || onTouchDevice()) {
            return null // tooltips on touch devices are handled separately
          }

          return ({
            html: `
            <p>
              ${mData.name}:
              <span style="color: rgba(${getColor(mData.dataPoint, boundaries)}); font-weight: bold;">
                ${(mData).formattedDataPoint}%
              </span>
            </p>`,
            style: TOOLTIP_COMMON_STYLE,
          })
        }}
        onClick={({ object: mData, x, y }) => {
          if (!isMunicipalityData(mData)) {
            setLastTapInfo(null)
            return
          }
          if (onTouchDevice()) {
            setLastTapInfo({ x, y, mData }) // trigger mobile tooltip display
            return
          }
          router.push(`/kommun/${mData.name.toLowerCase()}`)
        }}
        onViewStateChange={({ viewState }) => {
          setLastTapInfo(null)
          return enforceMapBounds(viewState)
        }}
        layers={[municipalityLayer]}
      // FIXME needs to be adapted to mobile before reintroducing
      /* onViewStateChange={({ viewState }) => {
      viewState.longitude = Math.min(MAP_RANGE.lon[1], Math.max(MAP_RANGE.lon[0], viewState.longitude))
      viewState.latitude = Math.min(MAP_RANGE.lat[1], Math.max(MAP_RANGE.lat[0], viewState.latitude))
      return viewState
    }} */
      />
      {lastTapInfo && <MobileTooltip tInfo={lastTapInfo} boundaries={boundaries} />}
      {children}
    </DeckGLWrapper>
  )
}

export default Map
