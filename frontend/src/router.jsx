// 1️⃣ PURPOSE (system terms)
// Make the Evaluation Dashboard reachable via a URL and navigation.
// This step:
// maps a route → Evaluation.jsx
// does not add logic
// does not touch state or APIs

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Documents from "./pages/Documents";
import Pipelines from "./pages/Pipelines";
import Evaluation from "./pages/Evaluation";
import Experiments from "./pages/Experiments";
import Analytics from "./pages/Analytics";

export default function AppRouter(){
    return (
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/documents" element={<Documents/>}/>
                <Route path="/pipelines" element={<Pipelines/>}/>
                <Route path="/evaluation" element={<Evaluation/>}/>
                <Route path="/experiments" element={<Experiments/>}/>
                <Route path="/analytics" element={<Analytics/>}/>
            </Routes>
    )
}