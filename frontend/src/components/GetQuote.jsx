import React from 'react'
import { useState } from 'react'

const GetQuote = ({ isOpen, onClose }) => {
  const modalStyle = {
    display: isOpen ? 'block' : 'none',
  }

  const [formData, setFormData] = useState({ name: '', email: '', phone: '', message: '', industry: '', company_website: '', facebook: '', instagram: '', linkedin: '', goals: '', company_name: '' })
  const [formErrors, setFormErrors] = useState({name: '', email: '', phone: '', industry: '', company_website: '', goals: '', company_name: ''})
  const [currentPage, setCurrentPage] = useState(0)
  // const [dropdownExtended, setDropdownExtended] = useState(false)

  const validate = (page) => {
    let errors = {}
    switch (page) {
      case 0:
        // Validate fields on page 1
        if (!formData.company_name.trim()) {
          errors.company_name = 'Company name is required'
        }
        if (!formData.company_website.trim()) {
          errors.company_website = 'Website link is required'
        } else {
          const urlPattern = /^(https?):\/\/[^\s/$.?#].[^\s]*$/
          const isValidUrl = urlPattern.test(formData.company_website)
          if (!isValidUrl){
            errors.company_website = 'Please enter a valid URL starting with http:// or https://'
          }
        }
        if (!formData.industry.trim()) {
          errors.industry = 'Industry is required'
        }
        if (!formData.goals.trim()) {
          errors.goals = 'Goals are required'
        }
        break
      case 2:
        if (!formData.name.trim()) {
          errors.name = 'Name is required'
        }
        if (!formData.email.trim()) {
          errors.email = 'Email is required'
        } else {
          const emailPattern = /^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/gm
          const isValidEmail = emailPattern.test(formData.email)
          if (!isValidEmail) {
            errors.email = 'Please enter a valid email address.'
          }
        }
        if (!formData.phone.trim()) {
          errors.phone = 'Phone is required'
        }
        break
      default:
        break
    }
    if (Object.keys(errors).length > 0) {
      setFormErrors({ ...formErrors, ...errors })
      return false
    }
    return true
  }

  const handleNextPage = (e) => {
    e.preventDefault()
    if (validate(currentPage)) {
      setCurrentPage(currentPage + 1)
    }
    // setCurrentPage(currentPage + 1)
  }

  const handlePreviousPage = (e) => {
    e.preventDefault()
    setCurrentPage(currentPage - 1)
  }

  const handleInputChange = (e) => {
    e.preventDefault()
    const {name, value} = e.target
    setFormData({ ...formData, [name]: value})

    if (name in formErrors) {
      setFormErrors({ ...formErrors, [name]: ''})
    }
  }

  const handleClose = (e) => {
    e.preventDefault()
    setCurrentPage(0)
    onClose()
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate(currentPage)) {
      return
    }
    console.log("Form data: ", formData)
    // setFormData({ name: '', email: '', phone: '', message: '', industry: '', company_website: '', facebook: '', instagram: '', linkedin: '', budget: '', goals: '' })
    // setCurrentPage(3)
    try {
      const response = await fetch('/api/contact-lead/', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      if (response.ok){
        setFormData({ name: '', email: '', phone: '', message: '', industry: '', company_website: '', facebook: '', instagram: '', linkedin: '', budget: '', goals: '', company_name: '' })
        const response_json = await response.json()
        console.log("message:", response_json.message)
        setCurrentPage(3)
      } else {
        const error = await response.json()
        console.error('Request Error:', error)
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const pages = [
    // Page 1
    (
      <>
        <div className="row">
          <div className="col-12">
            <div className="section-title mb-20">
              <h2 className="title text-dark">Tell us about Your Company.</h2>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <form>
              <div className="row row-gutter-20">
                <div className="col-12 mt-20">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>Company Name</h6></label>
                    <input className="form-control" type="text" name="company_name" value={formData.company_name} onChange={handleInputChange} />
                    {formErrors.company_name && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.company_name}</span>}
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>Company Website</h6></label>
                    <input className="form-control" type="url" name="company_website" value={formData.company_website} onChange={handleInputChange} />
                    {formErrors.company_website && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.company_website}</span>}
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>What industry do you operate in?</h6></label>
                    <input className="form-control" type="text" name="industry" value={formData.industry} onChange={handleInputChange} />
                    {formErrors.industry && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.industry}</span>}
                    {/* <div className="dropdown">
                      <button className="btn btn-light dropdown-toggle" type="button" onClick={() => {setDropdownExtended(!dropdownExtended)}} id="dropdownMenuButton" aria-expanded={dropdownExtended} style={{width: '100%'}}>
                        {formData.industry ? formData.industry : "Industry"}
                      </button>
                      <ul className={`dropdown-menu ${dropdownExtended ? 'show' : ''}`} style={{width: '100%'}}>
                        <li><a className="dropdown-item" href="#" onClick={(e) => {e.preventDefault(); setFormData({...formData, industry: "Industry 1"}) setDropdownExtended(false)}}>Industry 1</a></li>
                        <li><a className="dropdown-item" href="#" onClick={(e) => {e.preventDefault(); setFormData({...formData, industry: "Industry 2"}) setDropdownExtended(false)}}>Industry 2</a></li>
                        <li><a className="dropdown-item" href="#" onClick={(e) => {e.preventDefault(); setFormData({...formData, industry: "Industry 3"}) setDropdownExtended(false)}}>Industry 3</a></li>
                      </ul>
                    </div> */}
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>Your Goals</h6></label>
                    <textarea className="p-2" style={{minHeight: "50px"}} name="goals" rows={3} value={formData.goals} onChange={handleInputChange}></textarea>
                    {formErrors.goals && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.goals}</span>}
                  </div>
                </div>
                <div className="row mb-20 fixed-bottom justify-content-end">
                  <div className="col-6 text-center">
                    <div className="form-group mb-0">
                      <button className="btn btn-theme fixed-bottom" onClick={handleNextPage}>Next <i className="icofont-long-arrow-right"></i></button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </>
    ),
    // Page 2
    (
      <>
        <div className="row">
          <div className="col-12">
            <div className="section-title mb-40">
              <h2 className="title text-dark">Company Socials.</h2>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <form>
              <div className="row row-gutter-20">
                <div className="col-12">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>Facebook</h6></label>
                    <input className="form-control" type="text" name="facebook" value={formData.facebook} onChange={handleInputChange} />
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>Instagram</h6></label>
                    <input className="form-control" type="text" name="instagram" value={formData.instagram} onChange={handleInputChange} />
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                    <label className="form-label text-dark"><h6>LinkedIn</h6></label>
                    <input className="form-control" type="text" name="linkedin" value={formData.linkedin} onChange={handleInputChange} />
                  </div>
                </div>
                <div className="row fixed-bottom mb-20">
                  <div className="col text-center">
                    <div className="form-group mb-0">
                      <button className="btn btn-theme fixed-bottom" onClick={handlePreviousPage}><i className="icofont-long-arrow-left"></i> Previous</button>
                    </div>
                  </div>
                  <div className="col text-center">
                    <div className="form-group mb-0">
                      <button className="btn btn-theme fixed-bottom" onClick={handleNextPage}>Next <i className="icofont-long-arrow-right"></i></button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </>
    ),
    // Page 3
    (
      <>
        <div className="row">
          <div className="col-12">
            <div className="section-title mb-40">
              <h2 className="title text-dark">Get In Touch.</h2>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <form>
              <div className="row row-gutter-20">
                <div className="col-12">
                  <div className="form-group">
                  <label className="form-label text-dark"><h6>Name</h6></label>
                    <input className="form-control" type="text" name="name" value={formData.name} onChange={handleInputChange} />
                    {formErrors.name && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.name}</span>}
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                  <label className="form-label text-dark"><h6>Email</h6></label>
                    <input className="form-control" type="email" name="email" value={formData.email} onChange={handleInputChange} />
                    {formErrors.email && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.email}</span>}
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group">
                  <label className="form-label text-dark"><h6>Phone</h6></label>
                    <input className="form-control" type="text" name="phone" value={formData.phone} onChange={handleInputChange} />
                    {formErrors.phone && <span style={{ color: "red", fontSize: "small" }}>*{formErrors.phone}</span>}
                  </div>
                </div>
                <div className="col-12">
                  <div className="form-group mb-0">
                  <label className="form-label text-dark"><h6>Message</h6></label>
                    <textarea name="message" style={{minHeight: "50px"}} value={formData.message} onChange={handleInputChange}></textarea>
                  </div>
                </div>
                <div className="row fixed-bottom mb-20">
                  <div className="col text-center">
                    <div className="form-group mb-0">
                      <button className="btn btn-theme fixed-bottom" onClick={handlePreviousPage}><i className="icofont-long-arrow-left"></i> Previous</button>
                    </div>
                  </div>
                  <div className="col text-center">
                    <div className="form-group mb-0">
                      <button className="btn btn-theme fixed-bottom" onClick={handleSubmit}>Submit <i className="icofont-long-arrow-right"></i></button>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </>
    ),
    // Thank you page
    (
      <div className="row d-flex justify-content-center align-items-center" style={{ height: '100%' }}>
        <div className="col-12 text-center">
          <div className="section-title mb-40">
            <h1 className="title text-dark">We will get back to you shortly. Thank You!</h1>
          </div>
        </div>
      </div>
    )
  ]
// industry, budget, goal, social media
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12">
          <div className="overlay contact-form" style={modalStyle} onClick={handleClose}>
            <div className="popup contact-form-wrapper" onClick={(e) => e.stopPropagation()}>
              <span className="close-button" onClick={handleClose}><i className="icofont-close"></i></span>
              {pages[currentPage]}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GetQuote
