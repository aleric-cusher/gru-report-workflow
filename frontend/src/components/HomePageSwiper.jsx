import { useEffect } from "react";


const HomePageSwiper = () => {

  useEffect(() => {
    const homeSlider = new Swiper('.home-slider-container', {
      slidesPerView: 1,
      loop: true,
      spaceBetween: 30,
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
      effect: 'fade',
      fadeEffect: {
        crossFade: true,
      },
      navigation: {
        nextEl: '.home-slider-container .swiper-button-next',
        prevEl: '.home-slider-container .swiper-button-prev',
      },
    });

    // Background Image
    $('[data-bg-img]').each(function() {
      $(this).css('background-image', 'url(' + $(this).data("bg-img") + ')');
    });
    // Background Color
    $('[data-bg-color]').each(function() {
      $(this).css('background-color', $(this).data("bg-color"));
    });

    return () => {
      homeSlider.destroy();
    };
  }, []);

  return (
    <section className="home-slider-area slider-default">
      <div className="home-slider-content">
        <div className="swiper-container home-slider-container">
          <div className="swiper-wrapper home-slider">
            {/* <!-- Start Slide Item --> */}
            <div className="swiper-slide home-slider-item" data-swiper-autoplay="5000" data-bg-img="/assets/img/slider/bg1.jpg">
              <div className="slider-content-area">
                <div className="content">
                  <div className="subtitle-content">
                    <img src="/assets/img/shape/line1.png" alt="Virtuf-HasTech" />
                    <h6>Since 2023</h6>
                  </div>
                  <div className="tittle-wrp">
                    <h2>Seeking <span>profitability?</span></h2>
                  </div>
                  <p>Get fine-grained control over spends and audiences.</p>
                  <a href="/services" className="btn btn-theme btn-theme-color2">All Services <i className="icon icofont-long-arrow-right"></i></a>
                  {/* <!-- <a className="btn-play play-video-popup" href="https://player.vimeo.com/video/174392490?dnt=1&amp;app_id=122963"><span className="icon"><img src="//assets/img/icons/play.png" alt="Virtuf-HasTech"></span></a> --> */}
                </div>
                <div className="layer-style">
                  {/* <!-- <div className="thumb">
                    <img src="/assets/img/slider/1.jpg" alt="Virtuf-HasTech" />
                  </div> --> */}
                  {/* <!-- <div className="success-rate"><div className="content">98% <span>Successful Project</span></div></div> --> */}
                  {/* <!-- <div className="trusted-clients-content">
                    <span>Trusted <br>Clients</span>
                    <ul className="clients-list">
                      <li><img src="/assets/img/testimonial/clients1.png" alt="Virtuf-HasTech"></li>
                      <li><img src="/assets/img/testimonial/clients2.png" alt="Virtuf-HasTech"></li>
                      <li><img src="/assets/img/testimonial/clients3.png" alt="Virtuf-HasTech"></li>
                      <li><img src="/assets/img/testimonial/clients4.png" alt="Virtuf-HasTech"> <span>230+</span></li>
                    </ul>
                  </div> --> */}
                  <div className="shape-style1">
                    <img src="/assets/img/shape/1.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style2">
                    <img src="/assets/img/shape/2.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style3">
                    <img src="/assets/img/shape/3.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style4">
                    <img src="/assets/img/shape/4.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style5">
                    <img src="/assets/img/shape/5.png" alt="Virtuf-HasTech" />
                  </div>
                </div>
              </div>
            </div>
            {/* <!-- End Slide Item --> */}

            {/* <!-- Start Slide Item --> */}
            <div className="swiper-slide home-slider-item" data-swiper-autoplay="5000" data-bg-img="/assets/img/slider/bg1.jpg">
              <div className="slider-content-area">
                <div className="content">
                  <div className="subtitle-content">
                    <img src="/assets/img/shape/line1.png" alt="Virtuf-HasTech" />
                    <h6>Since 2023</h6>
                  </div>
                  <div className="tittle-wrp">
                    <h2>Scaling up your <span>presence?</span></h2>
                  </div>
                  <p>We help you with growing your reach & visibility.</p>
                  <a href="/services" className="btn btn-theme btn-theme-color2">All Services <i className="icon icofont-long-arrow-right"></i></a>
                  {/* <!-- <a className="btn-play play-video-popup" href="https://player.vimeo.com/video/174392490?dnt=1&amp;app_id=122963"><span className="icon"><img src="//assets/img/icons/play.png" alt="Virtuf-HasTech"></span></a> --> */}
                </div>
                <div className="layer-style">
                  {/* <!-- <div className="thumb">
                    <img src="/assets/img/slider/2.jpg" alt="Virtuf-HasTech">
                  </div> --> */}
                  {/* <!-- <div className="success-rate"><div className="content">98% <span>Customer Satisfaction</span></div></div> --> */}
                  {/* <!-- <div className="trusted-clients-content">
                    <span>Trusted <br>Clients</span>
                    <ul className="clients-list">
                      <li><img src="/assets/img/testimonial/clients1.png" alt="Virtuf-HasTech"></li>
                      <li><img src="/assets/img/testimonial/clients2.png" alt="Virtuf-HasTech"></li>
                      <li><img src="/assets/img/testimonial/clients3.png" alt="Virtuf-HasTech"></li>
                      <li><img src="/assets/img/testimonial/clients4.png" alt="Virtuf-HasTech"> <span>230+</span></li>
                    </ul>
                  </div> --> */}
                  <div className="shape-style1">
                    <img src="/assets/img/shape/1.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style2">
                    <img src="/assets/img/shape/2.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style3">
                    <img src="/assets/img/shape/3.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style4">
                    <img src="/assets/img/shape/4.png" alt="Virtuf-HasTech" />
                  </div>
                  <div className="shape-style5">
                    <img src="/assets/img/shape/5.png" alt="Virtuf-HasTech" />
                  </div>
                </div>
              </div>
            </div>
            {/* <!-- End Slide Item --> */}
          </div>
          {/* <!-- Add Arrows --> */}
          <div className="swiper-button-next"><i className="icofont-rounded-double-right"></i></div>
          <div className="swiper-button-prev"><i className="icofont-rounded-double-left"></i></div>
        </div>
      </div>
      <div className="home-slider-sidebar" data-aos="fade-zoom-in" data-aos-duration="1300">
        <div className="social-icon">
          <a href="#/"><i className="icofont-facebook"></i></a>
          <a href="#/"><i className="icofont-skype"></i></a>
          <a href="#/"><i className="icofont-twitter"></i></a>
        </div>
      </div>
    </section>
  )
}

export default HomePageSwiper
