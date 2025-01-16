import { GetServerSideProps } from 'next'
import { ReactElement } from 'react'
import styled from 'styled-components'
import Image from 'next/image'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import MetaTags from '../../components/MetaTags'
import { H2, H4, Paragraph } from '../../components/Typography'
import PageWrapper from '../../components/PageWrapper'
import Layout from '../../components/Layout'
import Footer from '../../components/Footer/Footer'
import { Grid, GridImage, GridItem } from '../../components/shared'
import { ONE_WEEK_MS } from '../../utils/shared'

const Ola = '/team/ola.jpg'
const Frida = '/team/frida.jpg'
const Elvira = '/team/elvira.jpg'
const Samuel = '/team/samuel.png'
const Alex = '/team/alex.jpg'
const Christian = '/board/christian.jpg'

const Container = styled.section`
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
`

const PaddedParagraph = styled(Paragraph)`
  padding-bottom: 24px;
`

const SocialMediaContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 12px;
`

const RoundedImage = styled(Image)`
  border-radius: 16px;
  margin: 8px 0;
  max-width: 100%;
  height: auto;
`

function InEnglish() {
  return (
    <>
      <MetaTags title="In English" description="Klimatkollen in English" />
      <PageWrapper>
        <Container>
          <H2>About us</H2>
          <Paragraph>
            Klimatkollen (Climate Checker) is a Swedish open source platform visualizing
            climate data for citizens.
          </Paragraph>
          <Paragraph>
            We believe that data transparency and citizen engagement are key to generating
            the public pressure needed to make sure local governments and companies cut
            emissions in line with the Paris Agreement.
          </Paragraph>
          <Paragraph>
            As proud winners of the
            {' '}
            <a
              href="https://blog.google/outreach-initiatives/sustainability/boosting-sustainable-solutions-from-sweden/"
              target="_blank"
              rel="noreferrer"
            >
              2023 Google.org Impact Challenge
            </a>
            , we will be scaling up and supercharging our citizen platform with AI,
            allowing us to add corporate emissions data and new features to analyze and
            compare climate action across local governments and companies.
          </Paragraph>
          <PaddedParagraph>
            Read more about the project
            {' '}
            <a
              // eslint-disable-next-line max-len
              href="https://www.mynewsdesk.com/se/klimatbyraan/pressreleases/klimatkollen-faar-maangmiljonstoed-fraan-google-punkt-org-foer-att-oeka-oeppenheten-om-foeretagens-utslaepp-3284663"
              target="_blank"
              rel="noreferrer"
            >
              here
            </a>
            {' '}
            (in Swedish).
          </PaddedParagraph>
          <H2>Our team</H2>
          <Grid>
            <GridItem>
              <GridImage src={Frida} alt="Frida Berry Eklund" width="200" height="200" />
              <b>Frida Berry Eklund, Co-founder</b>
              Senior climate communications specialist and co-founder of several climate
              initiatives, including the international platform, Our Kids’ Climate. She’s
              also an author and public speaker, as well as a EU Climate Pact Ambassador
              and Climate Reality Leader.
              {' '}
              <SocialMediaContainer>
                <a
                  href=" https://www.linkedin.com/in/fridaberryeklund/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/linkedin_white.svg"
                    alt="LinkedIn logo"
                    width="24"
                    height="24"
                  />
                </a>
                <a
                  href="https://twitter.com/klimatfrida"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/x_white.svg"
                    alt="X logo"
                    width="24"
                    height="24"
                  />
                </a>
              </SocialMediaContainer>
            </GridItem>
            <GridItem>
              <GridImage src={Ola} alt="Ola Spännar" width="200" height="200" />
              <b>Ola Spännar, Co-founder</b>
              Senior marketing and communications executive, previously head of
              Communications and Campaigns for the Swedish Centre Party, program director
              at Berghs School of Communication and Account Director at Forsman &
              Bodenfors.
              <SocialMediaContainer>
                <a
                  href=" https://www.linkedin.com/in/ospannar/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/linkedin_white.svg"
                    alt="LinkedIn logo"
                    width="24"
                    height="24"
                  />
                </a>
                <a href="https://twitter.com/olaspannar" target="_blank" rel="noreferrer">
                  <Image
                    src="/icons/some/x_white.svg"
                    alt="X logo"
                    width="24"
                    height="24"
                  />
                </a>
              </SocialMediaContainer>
            </GridItem>
            <GridItem>
              <GridImage src={Elvira} alt="Elvira Boman" width="200" height="200" />
              <b>Elvira Boman, Tech Lead</b>
              Teach Lead at Klimatkollen and Full Stack Developer and Engineering
              Physicist at Precisit. Extensive experience in green and circular tech at
              multiple award winning startups, including Deedster, and part of the
              leadership team at IT consultancy firm Precisit.
              <SocialMediaContainer>
                <a
                  href=" https://www.linkedin.com/in/elviraboman/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/linkedin_white.svg"
                    alt="LinkedIn logo"
                    width="24"
                    height="24"
                  />
                </a>
              </SocialMediaContainer>
            </GridItem>
            <GridItem>
              <GridImage src={Samuel} alt="Samuel Plumppu" width="200" height="200" />
              <b>Samuel Plumppu, Frontend Lead</b>
              Fullstack Developer with a passion for open source and for creating digital
              solutions that bring value to people and society. Previously worked with
              early stage startups and non-profits, including We Don’t Have Time.
              <SocialMediaContainer>
                <a
                  href=" https://www.linkedin.com/in/samuelplumppu/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/linkedin_white.svg"
                    alt="LinkedIn logo"
                    width="24"
                    height="24"
                  />
                </a>
              </SocialMediaContainer>
            </GridItem>
            <GridItem>
              <GridImage src={Alex} alt="Alexandra Palmquist" width="200" height="200" />
              <b>Alexandra Palmquist, Climate Data</b>
              Environmental scientist with a focus on climate and corporate data. Previous
              experience with the UN in Latin America, now well-established in
              Stockholm&apos;s tech startup scene to drive climate transition.
              <SocialMediaContainer>
                <a
                  href="https://www.linkedin.com/in/alexandra-palmquist-46969946/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/linkedin_white.svg"
                    alt="LinkedIn logo"
                    width="24"
                    height="24"
                  />
                </a>
              </SocialMediaContainer>
            </GridItem>
            <GridItem>
              <GridImage
                src={Christian}
                alt="Christian Landgren"
                width="200"
                height="200"
              />
              <b>Christian Landgren, AI Lead</b>
              Awarded developer, digital entrepreneur and one of Sweden’s most influential
              people in tech. Founder of digital innovation agency Iteam och co-founder of
              Öppna skolplattformen. Frequent speaker in AI and digital innovation and
              advisor to the Swedish Government.
              <SocialMediaContainer>
                <a
                  href="https://www.linkedin.com/in/christianlandgren/"
                  target="_blank"
                  rel="noreferrer"
                >
                  <Image
                    src="/icons/some/linkedin_white.svg"
                    alt="LinkedIn logo"
                    width="24"
                    height="24"
                  />
                </a>
              </SocialMediaContainer>
            </GridItem>
          </Grid>
          <H4>Want to use your skills for climate impact?</H4>
          <PaddedParagraph>
            We are currently looking for people that share our vision and want to help us
            grow. We’re especially interested in AI aficionados, data visualizers, UX
            specialists and climate data scientists. Please write us a message at
            {' '}
            <a href="mailto:hej@klimatkollen.se">hej@klimatkollen.se</a>
            .
          </PaddedParagraph>
          <H4>Interested in taking Klimatkollen to your country?</H4>
          <PaddedParagraph>
            Drop us a line if you want to hear more about us or collaborate. We are
            especially looking for co-funders and partner organisations in high-emitting
            countries, with an interest in climate data transparency and using tech and AI
            for good.
          </PaddedParagraph>
          <H2>Klimatkollen receives support from Google.org Impact Challenge</H2>
          <RoundedImage
            src="/board/impact_challenge.png"
            width={2000}
            height={1125}
            alt="Klimatkollen receives support from Google.org Impact Challenge"
          />
          <Paragraph>
            In November 2023, Klimatkollen was one of two Swedish recipients of the
            {' '}
            <a
              href="https://blog.google/outreach-initiatives/sustainability/boosting-sustainable-solutions-from-sweden/"
              target="_blank"
              rel="noreferrer"
            >
              Google.org Impact Challenge: Tech for Social Good
            </a>
            .
          </Paragraph>
          <Paragraph>
            During 2024–2026 we will build and integrate AI solutions into our platform,
            allowing for more and better climate data availability for citizens,
            increasing transparency of municipalities, governments and companies to cut
            emissions in line with the Paris Agreement.
          </Paragraph>
          <Paragraph>
            A key focus of the project is to increase the public availability and
            transparency of corporate climate data, making it easier for citizens to know
            if a company is in line with the Paris Agreement, or not.
          </Paragraph>
          <Paragraph>
            Companies are part of the problem as well as the solutions to climate change.
            In 2019–2020, large and medium sized Swedish companies emitted a whopping
            {' '}
            <a
              href="https://www.regeringen.se/contentassets/4a8366fdf6d84c2f929ab6e4a216e23f/sveriges-globala-klimatavtryck-sou-202215.pdf"
              target="_blank"
              rel="noreferrer"
            >
              250 million tonnes of CO2
            </a>
            , five times the amount of our territorial emissions.
          </Paragraph>
          <Paragraph>
            There is a big gap between what companies say and what they actually do, to
            bring emissions down. And it is hard for ordinary citizens to know what’s
            greenwashing and real action.
          </Paragraph>
          <Paragraph>
            Our AI solutions will increase both quantity and quality of climate data
            freely available to citizens, driving interaction and action both on and
            beyond our platform.
          </Paragraph>
          <PaddedParagraph>
            <b>Want to know more?</b>
            {' '}
            Please drop us a line at
            {' '}
            <a href="mailto:hej@klimatkollen.se">hej@klimatkollen.se</a>
            .
          </PaddedParagraph>
          <H2>Klimatkollen today</H2>
          <RoundedImage
            src="/board/whole_board.jpg"
            alt="Klimatkollen board"
            width="3000"
            height="2000"
          />
          <Paragraph>
            Klimatkollen gives citizens knowledge about how Sweden’s 290 municipalities
            are tracking compared to the Paris Agreement. We do this by presenting
            essential climate data in a simple and shareable format.
          </Paragraph>
          <Paragraph>
            Our data comes from a mix of sources, such as governmental databases, research
            institutions and other public sources, like Wikidata. We also enlist the help
            of citizens to crowdsource data.
          </Paragraph>
          <Paragraph>
            We use communication and visualisations to make data understandable, media
            outreach to contribute to a fact-based climate debate, and collaboration with
            partner organisations to inform and engage citizens.
          </Paragraph>
          <Paragraph>
            We work through – and with – partners across civil society, the corporate
            sector, media and research institutions. See some of our partners below.
          </Paragraph>
          <Paragraph>
            Klimatkollen was founded in 2021, by Frida Berry Eklund and Ola Spännar with
            the support of
            {' '}
            <a href="www.wwf.se" target="_blank" rel="noreferrer">
              WWF
            </a>
            ,
            {' '}
            <a href="www.climateview.global" target="_blank" rel="noreferrer">
              ClimateView
            </a>
            ,
            {' '}
            <a href="www.klimatklubben.se" target="_blank" rel="noreferrer">
              Klimatklubben
            </a>
            , Argand,
            {' '}
            <a href="https://app.wedonthavetime.org/" target="_blank" rel="noreferrer">
              We Don’t Have Time
            </a>
            {' '}
            and
            {' '}
            <a href="https://varabarnsklimat.se/" target="_blank" rel="noreferrer">
              Våra barns klimat
            </a>
            .
          </Paragraph>
          <Paragraph>
            Klimatkollen is a platform for – and by – citizens, and we welcome
            contributions through
            {' '}
            <a
              href="https://github.com/Klimatbyran/"
              target="_blank"
              rel="noreferrer"
            >
              Github
            </a>
            {' '}
            and
            {' '}
            <a href="https://discord.gg/N5P64QPQ6v" target="_blank" rel="noreferrer">
              Discord
            </a>
            .
          </Paragraph>
          <PaddedParagraph>
            If you want to support our work, please do not hesitate to contact us via
            {' '}
            <a href="mailto:hej@klimatkollen.se">hej@klimatkollen.se</a>
            .
          </PaddedParagraph>
        </Container>
      </PageWrapper>
    </>
  )
}

export const getServerSideProps: GetServerSideProps = async ({ res, locale }) => {
  res.setHeader(
    'Cache-Control',
    `public, stale-while-revalidate=60, max-age=${ONE_WEEK_MS}`,
  )

  return {
    props: {
      ...(await serverSideTranslations(locale as string, ['common'])),
    },
  }
}

export default InEnglish

InEnglish.getLayout = function getLayout(page: ReactElement) {
  return (
    <>
      <Layout>{page}</Layout>
      <Footer />
    </>
  )
}
