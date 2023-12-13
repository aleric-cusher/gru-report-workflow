import React from 'react'
import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import GetQuote from './GetQuote'

const Header = () => {
  const location = useLocation()
  const { pathname } = location
  const current = pathname.split('/')[1]

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  return (
    <>
      <div>
        <GetQuote isOpen={isModalOpen} onClose={closeModal} />
      </div>

      <header className="header-area header-default sticky-header transparent">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-6 col-sm-3 col-md-3 col-lg-2 pr-0">
              <div className="header-logo-area">
                <Link to="/">
                  <img className="logo-main" src="/assets/img/logo.png" alt="Logo" />
                  <img className="logo-light" src="/assets/img/logo.png" alt="Logo" />
                </Link>
              </div>
            </div>
            <div className="col-6 col-sm-9 col-md-9 col-lg-10">
              <div className="header-align">
                <div className="header-navigation-area navigation-style-two">
                  <ul className="main-menu nav justify-content-center">
                    <li className={current === "" ? "active" : ""}><Link to="/">Home</Link></li>
                    <li  className={current === "about" ? "active" : ""}><Link to="/about">About</Link></li>

                    <li className={(current === "services" || current === "service-details") ? "has-submenu active" : "has-submenu"}><Link to="/services">Services</Link></li>

                    <li className={(current === "blog" || current === "blog-details") ? "has-submenu active" : "has-submenu"}><Link to="/blog">Blog</Link>
                      <ul className="submenu-nav">
                        <li><Link to="/blog">Blog Grid</Link></li>
                        <li><Link to="/blog-details">Blog Single</Link></li>
                      </ul>
                    </li>

                    <li className={current === "contact" ? "active" : ""}><Link to="/contact">Contact</Link></li>
                  </ul>
                </div>
                <div className="header-action-area">
                  <button className="btn-menu d-xl-none">
                    <span></span>
                    <span></span>
                    <span></span>
                  </button>
                  <button className="btn-theme btn-style" id="open-popup" onClick={openModal}>Get A Quote <i className="icon-style icofont-double-right"></i></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>
    </>
  )
}

export default Header
