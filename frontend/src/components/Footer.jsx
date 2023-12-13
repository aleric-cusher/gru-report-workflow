import React from 'react'

const Footer = () => {

  const handleScrollToTop = () => {
    $('html, body').animate({scrollTop : 0},800);
    return false;
  }

  return (
    <footer className="footer-area bg-img-cover" style={{backgroundImage: 'url("/assets/img/photos/bg-footer.jpg")'}} data-bg-img="/assets/img/photos/bg-footer.jpg">
      <div className="footer-bottom">
        <div className="container">
          <div className="footer-bottom-content">
            <div className="row align-items-center">
              <div className="col-md-5 col-lg-5 col-xl-4">
                <div className="widget-copyright">
                  <p>© 2023 by <span>Gruworks.com</span>. All Rights Reserved</p>
                </div>
              </div>
              <div className="col-md-5 col-lg-4 col-xl-4">
                <div className="widget-social-icons">
                <a href="#"><i className="icofont-facebook"></i></a>
                <a href="#"><i className="icofont-skype"></i></a>
                <a href="#"><i className="icofont-instagram"></i></a>
                <a href="#"><i className="icofont-twitter"></i></a>
                </div>
              </div>
              <div className="col-md-2 col-lg-1 offset-lg-2 col-xl-1 offset-xl-3">
                {/* <!--== Scroll Top Button ==--> */}
                <div className="scroll-to-top" onClick={handleScrollToTop}><img src="/assets/img/icons/arrow-top.png" alt="Icon-Image" /></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
