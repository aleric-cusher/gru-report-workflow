import React, { useEffect } from 'react'
import Preloader from '../components/Preloader'
import Header from '../components/Header'
import Footer from '../components/Footer'
import SideMenu from '../components/SideMenu'

const ContactPage = () => {
  useEffect(() => {
    AOS.init()
  }, [])

  useEffect(() => {
    $('[data-bg-img]').each(function() {
      $(this).css('background-image', 'url(' + $(this).data("bg-img") + ')');
    });
    // Background Color
    $('[data-bg-color]').each(function() {
      $(this).css('background-color', $(this).data("bg-color"));
    });
  }, [])

  return (
    <div className="wrapper contact-page-wrapper">
      <Preloader />
      <Header />

      <main className="main-content site-wrapper-reveal">
        {/* <!--== Start Page Title Area ==--> */}
        <section className="page-title-area" data-bg-img="/assets/img/photos/bg-page-title.jpg">
          <div className="container">
            <div className="row">
              <div className="col-lg-12">
                <div className="page-title-content">
                  <h2 className="title text-white">Contact Us</h2>
                  <div className="bread-crumbs"><img className="line-shape" src="/assets/img/shape/line-s3.png" alt="Virtuf-HasTech" /><a href="/index">Home<span className="breadcrumb-sep">//</span></a><span className="active">Contact</span></div>
                </div>
              </div>
            </div>
          </div>
          <div className="page-sidebar" data-aos="fade-right" data-aos-duration="1100">
            <div className="social-icon">
              <a href="#/"><i className="icofont-facebook"></i></a>
              <a href="#/"><i className="icofont-skype"></i></a>
              <a href="#/"><i className="icofont-twitter"></i></a>
            </div>
          </div>
          <div className="layer-shape">
            <img className="layer-shape-one" src="/assets/img/shape/1.png" alt="Virtuf-Image" />
            <img className="layer-shape-two" src="/assets/img/shape/4.png" alt="Virtuf-Image" />
            <img className="layer-shape-three" src="/assets/img/shape/5.png" alt="Virtuf-Image" />
            <img className="layer-shape-four" src="/assets/img/shape/3.png" alt="Virtuf-Image" />
          </div>
        </section>
        {/* <!--== End Page Title Area ==--> */}

        {/* <!--== Start Contact Area ==--> */}
        <section className="contact-area">
          <div className="contact-info-light" data-aos="fade-up" data-aos-duration="1000">
            <div className="contact-info-content">
              {/* <div className="contact-info-item">
                <div className="icon">
                  <img className="icon-img" src="/assets/img/icons/c1.png" alt="Icon">
                </div>
                <div className="content">
                  <h4>Call Us.</h4>
                  <img className="line-icon" src="/assets/img/shape/line-s1.png" alt="Icon">
                  <a href="tel://+00(88)123456789">+00 (88) 123 456 789</a>
                  <a href="tel://+88000111234567">+88 000 111 234 567</a>
                </div>
              </div> */}
              <div className="contact-info-item">
                <div className="icon">
                  <img className="icon-img" src="/assets/img/icons/c2.png" alt="Icon" />
                </div>
                <div className="content">
                  <h4>Email.</h4>
                  <img className="line-icon" src="/assets/img/shape/line-s1.png" alt="Icon" />
                  <a href="mailto://nik@gruworks.com">nik@gruworks.com</a>
                </div>
              </div>
              <div className="contact-info-item">
                <div className="icon">
                  <img className="icon-img" src="/assets/img/icons/c3.png" alt="Icon" />
                </div>
                <div className="content">
                  <h4>Location.</h4>
                  <img className="line-icon" src="/assets/img/shape/line-s1.png" alt="Icon" />
                  <p>GRUworks<br />273, 4th Main Rd, 1st Block Koramangala<br />Bengaluru, Karnataka</p>
                </div>
              </div>
            </div>
          </div>
          <div className="container">
            <div className="row">
              <div className="col-lg-12">
                <div className="contact-colunm" data-aos="fade-up" data-aos-duration="1000">
                  <div className="contact-map-area">
                    <iframe src="https://maps.google.com/maps/place?q=GRUworks%2C%20273%2C%204th%20Main%20Rd%2C%201st%20Block%20Koramangala%2C%20Koramangala%2C%20Bengaluru%2C%20Karnataka%20560034&z=15&output=embed" width="360" height="270" style={{border:0}}></iframe>
                  </div>
                  <div className="contact-form">
                    <form className="contact-form-wrapper" id="contact-form" action="http://whizthemes.com/mail-php/raju/arden/mail.php" method="post">
                      <div className="row">
                        <div className="col-lg-12">
                          <div className="section-title">
                            <div className="subtitle-content">
                              <img src="/assets/img/shape/line-s4.png" alt="Virtuf-HasTech" />
                              <h5 className="text-light">Contact Us</h5>
                            </div>
                            <h2 className="title text-light">Get In <span>Touch.</span></h2>
                            <div className="separator-line">
                              <img src="/assets/img/shape/line-s4.png" alt="Virtuf-HasTech" />
                              <img src="/assets/img/shape/line-s4.png" alt="Virtuf-HasTech" />
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="row">
                        <div className="col-lg-12">
                          <div className="row row-gutter-20">
                            <div className="col-md-12">
                              <div className="form-group">
                                <input className="form-control" type="text" name="con_name" placeholder="Name" />
                              </div>
                            </div>
                            <div className="col-md-12">
                              <div className="form-group">
                                <input className="form-control" type="email" name="con_email" placeholder="Email" />
                              </div>
                            </div>
                            <div className="col-md-12">
                              <div className="form-group">
                                <input className="form-control" type="text" name="con_phone" placeholder="Phone" />
                              </div>
                            </div>
                            <div className="col-md-12">
                              <div className="form-group mb-0">
                                <textarea name="con_message" placeholder="Message"></textarea>
                              </div>
                            </div>
                            <div className="col-md-12">
                              <div className="form-group mb-0">
                                <button className="btn btn-theme" type="submit">Submit Now <i className="icofont-long-arrow-right"></i></button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </form>
                  </div>
                  {/* <!-- Message Notification --> */}
                  <div className="form-message"></div>
                </div>
              </div>
            </div>
          </div>
        </section>
        {/* <!--== End Contact Area ==--> */}
      </main>

      <Footer />
      <SideMenu />
    </div>
  )
}

export default ContactPage
