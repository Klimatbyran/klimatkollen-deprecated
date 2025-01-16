import { ReactNode } from 'react'
import { TFunction } from 'next-i18next'

import { validDatasets } from './datasetDefinitions'

export type Image = {
  ImageUrl: string
  Description: string
}

// Companies

export type Metadata = {
  verifiedBy: {
    name: string
  } | null,
}

export type Scope3 = {
  statedTotalEmissions?: {
    total?: number
    metadata: Metadata
  } | null
  categories: { category: number, total: number }[]
  calculatedTotalEmissions: number
}

export type CompanyJsonData = {
  name: string
  description?: string
  wikidataId?: string
  reportingPeriods: Array<{
    emissions?: {
      scope1?: {
        total?: number
        metadata: Metadata
      }
      scope2?: {
        mb?: number
        metadata: Metadata
        calculatedTotalEmissions: number
      }
      scope3?: Scope3
      scope1And2: {
        total?: number
        metadata: Metadata
      }
      calculatedTotalEmissions: number
    }
    reportURL?: string
  }>
}

export type CompaniesJsonData = Array<CompanyJsonData>

export type CompanyEmissionsPerYear = {
  Scope1n2: number | null
  Scope3: number | null
}

export type Company = {
  Name: string
  Url: string
  WikiId: string | null
  Comment: string
  Emissions: CompanyEmissionsPerYear
}

// Municipalities

export type EmissionPerYear = {
  Year: number
  CO2Equivalent: number
}

export type EmissionSector = {
  Name: string
  Year: string
  CO2Equivalent: number
  SubSectors: Array<EmissionSector>
}

export type Emission = {
  EmissionPerYear: Array<EmissionPerYear>
  LargestEmissionSectors: Array<EmissionSector>
  HistoricalEmissionChangePercent: number
  HistoricalEmissionChangeRank: number | null
}

export type ApproximatedEmission = {
  EmissionPerYear: Array<EmissionPerYear>
  TotalCO2Emission: number | null
}

export type Budget = {
  CO2Equivalent: number
  BudgetPerYear: Array<EmissionPerYear>
}

export type Trend = {
  TrendPerYear: Array<EmissionPerYear>
  TrendCO2Emission: number
}

export type ClimatePlan = {
  Link: string
  YearAdapted: string
  Comment: string
}

export type Municipality = {
  County: string
  Name: string
  CoatOfArmsImage: Image | null
  Population: number | null
  Image: Image | null
  Budget: Budget
  HistoricalEmission: Emission
  PoliticalRule: Array<string> | null
  ApproximatedHistoricalEmission: ApproximatedEmission
  EmissionTrend: Trend
  NeededEmissionChangePercent: number
  HitNetZero: number | string
  BudgetRunsOut: string
  ElectricCars: number
  ElectricCarChangePercent: number
  ElectricCarChangeYearly: Array<number>
  ClimatePlan: ClimatePlan
  BicycleMetrePerCapita: number
  TotalConsumptionEmission: number
  ElectricVehiclePerChargePoints: number
  ProcurementScore: number
  ProcurementLink: string
}

export type DataDescriptionDataPoints = {
  rawDataPoint: (item: Municipality) => number | string | Date
  formattedDataPoint: (dataPoint: number | string | Date, t: TFunction) => string
  additionalDataPoint?: (item: Municipality) => string
}

export type DataDescription = {
  /** Short name for the dataset */
  name: string

  /** Longer title */
  title: string
  body: string
  source: string
  boundaries: number[] | string[] | Date[]
  labels: string[]
  labelRotateUp: boolean[]
  columnHeader: string
  dataPoints: DataDescriptionDataPoints
  sortAscending?: boolean
  stringsOnTop?: boolean // If true, the strings will be sorted to the top of the table
}

export type DatasetKey = (typeof validDatasets)[number]
export type DataDescriptions = Record<DatasetKey, DataDescription>

export type CurrentDataPoints = {
  name: string
  primaryDataPoint: number | string | Date
  formattedPrimaryDataPoint: string
  secondaryDataPoint?: string | null
}

export type MapProps = {
  data: Array<CurrentDataPoints>
  boundaries: number[] | string[] | Date[]
  children?: ReactNode
}

export type MunicipalityData = {
  name: string
  dataPoint: number
  formattedDataPoint: number
  geometry: [number, number][]
}

export type MunicipalityTapInfo = {
  x: number
  y: number
  mData: MunicipalityData
}
