import styled from 'styled-components'
import { devices } from '../../utils/devices'

const PartnerContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  justify-items: center;
  flex-wrap: wrap;
  align-items: center;
  width: 100%;
  margin-bottom: 48px;
  padding: 8px 16px;

  img {
    margin: 16px;
  }

  @media only screen and (${devices.tablet}) {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    justify-items: center;
    padding: 16px 32px;
  }
`

function Partners() {
  return (
    <PartnerContainer>
      <a href="https://www.climateview.global/" target="_blank" rel="noreferrer">
        <img
          src="/logos/partners/climateview.svg"
          width={90}
          height="auto"
          alt="ClimateView logo"
        />
      </a>
      <a href="https://researchersdesk.se/" target="_blank" rel="noreferrer">
        <img
          src="/logos/partners/researchersdesk-logo.svg"
          width="auto"
          height={60}
          alt="Researchers desk logo"
        />
      </a>
      <a href="https://www.klimatklubben.se/" target="_blank" rel="noreferrer">
        <img
          src="/logos/partners/klimatklubben.svg"
          width="auto"
          height={45}
          alt="Klimatklubben logo"
        />
      </a>
      <a href="https://exponentialroadmap.org/" target="_blank" rel="noreferrer">
        <img
          src="/logos/partners/exponential_roadmap.svg"
          width={105}
          height="auto"
          alt="Exponential Roadmap logo"
        />
      </a>
      <a href="https://www.climateainordics.com/" target="_blank" rel="noreferrer">
        <img
          src="/logos/partners/climateAiNordics.png"
          width={90}
          height="auto"
          alt="ClimateAiNordics logo"
        />
      </a>
    </PartnerContainer>
  )
}

export default Partners
