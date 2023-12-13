import { useEffect } from 'react'
import Preloader from '../components/Preloader'
import Header from '../components/Header'
import Footer from '../components/Footer'
import SideMenu from '../components/SideMenu'
import HomePageSwiper from '../components/HomePageSwiper'

const HomePage = () => {
  useEffect(() => {
    AOS.init()
  }, [])

  return (
    <div className="wrapper home-default-wrapper">
      <Preloader />
      <Header />

      <main className="main-content">
        <HomePageSwiper />
        {/* <!--== Start About Area ==--> */}
        <section className="about-area about-default-area">
          <div className="container">
            <div className="row">
              <div className="col-lg-5 md-text-center">
                <div className="layer-style" data-aos="fade-up" data-aos-duration="1000">
                  <div className="thumb tilt-animation">
                    <img src="/assets/img/about/01.jpg" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style1">
                      <img src="/assets/img/shape/circle-line1.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style2 scene">
                    <span className="scene-layer" data-depth="0.60">
                      <img src="/assets/img/shape/circle-shape1.png" alt="Virtuf-HasTech" />
                    </span>
                  </div>
                  <div className="experience-time">
                    <div className="content">32<sup>+</sup> <span>Years of Experience</span></div>
                  </div>
                </div>
              </div>
              <div className="col-lg-6 offset-lg-1">
                <div className="about-content">
                  <div className="section-title xs-text-center" data-aos="fade-up" data-aos-duration="1000">
                    <h2 className="title">We are <span>Invested</span> in Your Growth.</h2>
                    <div className="desc">
                      <p className="mt-20">We aspire to redefine growth consulting excellence.<br />
                        Our unique methodology revolves around close collaboration with clients, allowing us to continually discover and map an ever-evolving branding, outreach, marketing, and conversion strategy. We ensure the successful implementation of these strategies.
                      </p>
                    </div>
                  </div>
                  <div className="list-icon-style" data-aos="fade-up" data-aos-duration="1200">
                    <ul>
                      <li><i className="icon icofont-clock-time"></i> Save Your Time</li>
                      <li><i className="icon icofont-money-bag"></i> Earn More Money</li>
                      <li><i className="icon icofont-chart-growth"></i> Grow Business</li>
                      <li><i className="icon icofont-live-support"></i> 24/7 Support</li>
                      <li><i className="icon icofont-badge"></i> Trusted Partner</li>
                      <li><i className="icon icofont-unique-idea"></i> Innovative Ideas</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        {/* <!--== End About Area ==--> */}
      </main>

      <Footer />
      <SideMenu />
    </div>
  )
}

export default HomePage
