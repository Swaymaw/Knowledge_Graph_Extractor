import React from 'react'

export default function Header() {
  return (
    <nav className="navbar navbar-dark bg-dark">
        <a className="navbar-brand" href="/">
            <img src="/favicon.png" width="30" height="30" className="d-inline-block align-top" alt=""/>
            <div style={{minWidth:"10px", display: 'inline-block'}}></div>
            <p style={{display: 'inline-block'}}>Knowledge Graph Builder</p>
        </a>
    </nav>
  )
}
