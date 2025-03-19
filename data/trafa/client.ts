import { TRAFA_BASE_URL } from '.'

// bun run data/trafa/client.ts

type TrafaMeasure =
  | 'itrfslut'
  | 'avstslut'
  | 'nyregunder'
  | 'avregunder'
  | 'biltathet'
  | 'akumunyreg'

type TrafaFuel =
  | 'el'
  | 'elhybrid'
  | 'laddhybrid'
  | 'biodiesel'
  | 'gas'
  | 'bensin'
  | 'diesel'
  | 'ovriga'
  | 'totalt'

export const TrafaDataTargetCategory = {
  onTheRoad: 'Fordon på väg',
  communal: 'Fordon i län och kommuner',
  monthly: 'Fordon månadsstatistik',
} as const
const TrafaDataTarget = {
  onTheRoad: {
    buses: 't10011',
    bikes: 't10014',
    mopeds: 't10015',
    trailers: 't10017',
    tractors: 't10018',
    atvs: 't10019',
    drivingLicenses: 't10012',
    cars: 't10016',
    trucks: 't10013',
  },
  communal: {
    buses: 't10021',
    trucks: 't10023',
    cars: 't10026',
    other: 't10029',
  },
  monthly: {
    trucks: 't10033',
    cars: 't10036',
    other: 't10039',
  },
} as const

/**
 * Validates a comma-separated string of years.
 *  Checks if all the years in the array are valid.
 *  A valid year is defined as a year that is greater than or equal to 2000
 * and less than or equal to the current year.
 * @param commaSeparatedYearString - The string containing comma-separated years.
 * @returns An array of valid years.
 */
export const validYears = (commaSeperatedYearString: string) => {
  const years = commaSeperatedYearString.split(',').map((y) => parseInt(y, 10))
  const isValidYear = years.filter((y) => y >= 2000 && y <= new Date().getFullYear())
  return isValidYear || []
}

/**
 * Represents a Trafa client with various methods for configuring and building a query.
 * @example https://api.trafa.se/api/data?query=t10016|ar:2020|itrfslut|drivm:bensin
 * @url https://www.trafa.se/vagtrafik/fordon/?cw=1
 */
export class TrafaClient {
  /**
   * The category of the target data
   * @default 'onTheRoad'
   */
  private category: keyof typeof TrafaDataTarget

  /**
   * The target data to filter by
   */
  private target: string

  /**
   * The year to filter by, empty means all years
   */
  private year: number[] = []

  /**
   * The measure to filter by
   *
   * itrfslut : Antal i trafik
   *
   * avstslut : Antal avställda
   *
   * nyregunder : Antal nyregistreringar
   *
   * avregunder : Antal avregistreringar
   *
   * biltathet : Antal i trafik per 1000 invånare
   *
   * akumunyreg : Ackumulerat  nyregistreringar
   *
   * @default 'itrfslut'
   */
  private measure: TrafaMeasure[] = []

  /**
   * The fuel types to filter by, empty means all fuel types
   */

  private fuel: TrafaFuel[] = []

  public constructor() {
    this.year = []
    this.measure = ['itrfslut']
    this.fuel = []
    this.target = 't10016'
    this.category = 'onTheRoad'
  }

  setYear(y: string) {
    const years = validYears(y)
    this.year = years
    return this
  }

  setMeasure(m: TrafaMeasure[]) {
    this.measure = m
    return this
  }

  setFuel(f: TrafaFuel[]) {
    this.fuel = f
    return this
  }

  setTarget<T extends keyof typeof TrafaDataTarget>(params: {
    category: T
    target: keyof (typeof TrafaDataTarget)[T]
  }) {
    this.category = params.category
    this.target = TrafaDataTarget[params.category][params.target] as string
    return this
  }

  /**
   * Builds the query string for the TRAFA API based on the current state of the client.
   * @param withBaseUrl - Indicates whether to include the base URL in the returned query string.
   * @returns The constructed query string.
   * @default true
   */
  build() {
    const queryParts: string[] = [this.target, 'ar']

    if (this.year.length > 0) {
      queryParts[1] += `:${this.year.join(',')}`
    }

    if (this.measure.length > 0) {
      queryParts.push(this.measure.join('|'))
    }

    if (this.fuel.length > 0) {
      queryParts.push(
        `${this.category === 'communal' ? 'drivmedel' : 'drivm'}:${this.fuel.join(',')}`,
      )
    }

    if (this.category === 'communal') {
      queryParts.push('reglan', 'regkom')
    }
    return {
      query: queryParts.join('|'),
      url: `${TRAFA_BASE_URL}?query=${queryParts.join('|')}`,
    }
  }
}
