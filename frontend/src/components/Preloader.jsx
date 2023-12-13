import React from 'react'

const Preloader = () => {
  return (
    <div className="preloader-wrap">
      <div className="preloader">
        <span className="dot"></span>
        <div className="dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  )
}

export default Preloader
