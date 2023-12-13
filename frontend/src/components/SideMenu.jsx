import React, { useEffect } from 'react'
import { Link } from 'react-router-dom'

const SideMenu = () => {

  useEffect(() => {
    // Get the necessary DOM elements
    const canvasWrapper = $(".off-canvas-wrapper");
    const btnMenu = $(".btn-menu");
    const closeActions = $(".close-action > .btn-close, .off-canvas-overlay");

    // Attach the click event handler for opening the off-canvas menu
    btnMenu.on('click', function () {
      canvasWrapper.addClass('active');
      $("body").addClass('fix');
    });

    // Attach the click event handler for closing the off-canvas menu
    closeActions.on('click', function () {
      canvasWrapper.removeClass('active');
      $("body").removeClass('fix');
    });

    $('.main-menu').slicknav({
      appendTo: '.res-mobile-menu',
      closeOnClick: true,
      removeClasses: true,
      closedSymbol: '<i class="icon_plus"></i>',
      openedSymbol: '<i class="icon_minus-06"></i>'
    });

    // Clean up event handlers when the component unmounts
    return () => {
      btnMenu.off('click');
      closeActions.off('click');
    };
  }, []);

  return (
    <aside className="off-canvas-wrapper">
      <div className="off-canvas-inner">
        <div className="off-canvas-overlay"></div>
        {/* <!-- Start Off Canvas Content Wrapper --> */}
        <div className="off-canvas-content">
          {/* <!-- Off Canvas Header --> */}
          <div className="off-canvas-header">
            <div className="logo-area">
              <Link to="/"><img src="/assets/img/logo.png" alt="Logo" /></Link>
            </div>
            <div className="close-action">
              <button className="btn-close"><i className="icofont-close"></i></button>
            </div>
          </div>

          <div className="off-canvas-item">
            {/* <!-- Start Mobile Menu Wrapper --> */}
            <div className="res-mobile-menu menu-active-two">
              {/* <!-- Note Content Auto Generate By Jquery From Main Menu --> */}
            </div>
            {/* <!-- End Mobile Menu Wrapper --> */}
          </div>
          {/* <!-- Off Canvas Footer --> */}
          <div className="off-canvas-footer"></div>
        </div>
        {/* <!-- End Off Canvas Content Wrapper --> */}
      </div>
    </aside>
  )
}

export default SideMenu
