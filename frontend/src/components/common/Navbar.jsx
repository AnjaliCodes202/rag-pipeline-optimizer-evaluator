import React from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="app-navbar">
      <div className="nav-left">
        <span className="app-title">RAG Optimizer</span>
      </div>
      <div className="nav-right">
        <NavLink to="/documents">Documents</NavLink>
        <NavLink to="/pipelines">Pipelines</NavLink>
        <NavLink to="/evaluation">Evaluation</NavLink>
        <NavLink to="/analytics">Analytics</NavLink>
      </div>
    </nav>
  );
}
