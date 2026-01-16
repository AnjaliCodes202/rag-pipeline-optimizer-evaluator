import React from 'react'
import AppRouter from './router.jsx'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import './App.css'
import './styles/layout.css'
import Navbar from './components/common/Navbar.jsx';

export default function App(){
    return (
      <BrowserRouter>
          <Navbar/>
          <AppRouter/>
      </BrowserRouter>
    )
};

