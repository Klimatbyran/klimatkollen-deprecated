import { TRAFA_BASE_URL } from '../../data/trafa'
import { TrafaClient } from '../../data/trafa/client'

describe('TrafaClientImpl', () => {
  let client: TrafaClient

  beforeEach(() => {
    client = new TrafaClient()
  })

  it('should set default values', () => {
    const { url } = client.build()
    expect(url).toBe(`${TRAFA_BASE_URL}?query=t10016|ar|itrfslut`)
  })

  it('should set year using setYear method', () => {
    const { url } = client.setYear('2020,2021').build()
    expect(url).toBe(`${TRAFA_BASE_URL}?query=t10016|ar:2020,2021|itrfslut`)
  })

  it('should set measure using setMeasure method', () => {
    const { url } = client.setMeasure(['avregunder']).build()
    expect(url).toBe(`${TRAFA_BASE_URL}?query=t10016|ar|avregunder`)
  })

  it('should set fuel using setFuel method', () => {
    const { url } = client.setFuel(['bensin', 'el']).build()
    expect(url).toBe(`${TRAFA_BASE_URL}?query=t10016|ar|itrfslut|drivm:bensin,el`)
  })

  it('should set target using setTarget method', () => {
    const { url } = client.setTarget({ category: 'onTheRoad', target: 'cars' }).build()
    expect(url).toBe(`${TRAFA_BASE_URL}?query=t10016|ar|itrfslut`)
  })

  it('should build URL correctly with communal category', () => {
    const { url } = client.setTarget({ category: 'communal', target: 'cars' }).build()
    expect(url).toBe(`${TRAFA_BASE_URL}?query=t10026|ar|itrfslut|reglan|regkom`)
  })

  it('should return query without base url', () => {
    const { query } = client.setYear('2020,2021').build()
    expect(query).toBe('t10016|ar:2020,2021|itrfslut')
  })
})
