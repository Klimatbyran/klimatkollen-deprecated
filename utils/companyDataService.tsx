import { isNumber } from './shared'
import {
  CompaniesJsonData,
  Company,
  CompanyEmissionsPerYear,
  CompanyJsonData,
  type Scope3,
} from './types'

function getScope3Total({
  calculatedTotalEmissions,
  statedTotalEmissions,
  categories,
}: Scope3) {
  if (categories.length && calculatedTotalEmissions > 0) {
    return calculatedTotalEmissions
  }

  if (isNumber(statedTotalEmissions?.total)) {
    return statedTotalEmissions.total
  }
  return null
}

export function getLatestReportingPeriodWithEmissions(company: CompanyJsonData) {
  return company.reportingPeriods.find(({ emissions }) => Boolean(emissions))
}

export class CompanyDataService {
  companies: Array<Company> = []

  constructor() {
    this.loadCompanies()
  }

  private async loadCompanies() {
    try {
      const response = await fetch('https://api.klimatkollen.se/api/companies')

      if (!response.ok) {
        throw new Error('Failed to fetch data from the API', { cause: { status: response.status, statusText: response.statusText } })
      }

      const jsonData = (await response.json()) as CompaniesJsonData

      this.companies = jsonData
        .map((data: CompanyJsonData) => {
          const currentPeriod = getLatestReportingPeriodWithEmissions(data)
          const currentEmissions = currentPeriod?.emissions

          // If either scope 1 or scope 2 have verification, then we use them for the total.
          // Otherwise, we use the combined scope1And2 if it exists
          const Scope1n2 = ((Boolean(currentEmissions?.scope1?.metadata?.verifiedBy)
            || Boolean(currentEmissions?.scope2?.metadata?.verifiedBy)
            ? (currentEmissions?.scope1?.total ?? 0)
            + (currentEmissions?.scope2
              ?.calculatedTotalEmissions ?? 0)
            : currentEmissions?.scope1And2?.total)) ?? null

          const emissionsPerYear: CompanyEmissionsPerYear = {
            Scope1n2,
            Scope3: currentEmissions?.scope3 ? getScope3Total(currentEmissions.scope3) : null,
          }

          return {
            Name: data.name,
            Url: currentPeriod?.reportURL ?? '',
            WikiId: data.wikidataId,
            Comment: data.description,
            Emissions: emissionsPerYear,
          } as Company
        })
    } catch (error) {
      throw new Error('Failed to retrieve company data from the API', { cause: error })
    }
  }

  public async getCompanies(): Promise<Array<Company>> {
    if (this.companies.length < 1) {
      await this.loadCompanies()
    }
    return this.companies
  }

  public getCompany(name: string): Company | undefined {
    return this.companies.find(
      (company) => company.Name.toLowerCase() === name.toLowerCase(),
    )
  }
}
