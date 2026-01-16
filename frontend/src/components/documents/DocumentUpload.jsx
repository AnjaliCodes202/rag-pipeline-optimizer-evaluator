// 1️⃣ PURPOSE (system terms)
// This component:
// lets user upload a file (PDF / TXT / DOCX)
// sends file to backend /documents/upload
// receives extracted text
// stores extracted text in Zustand (documentText)
// It does not:
// chunk
// embed
// evaluate

// DocumentUpload.jsx
//  → documentApi.js
//    → backend /documents/upload
//      → text extraction
//    → response (text)
//  → Zustand.setDocumentText()


import React, { useState } from "react";
import {uploadDocument} from "../../services/documentApi";
import {useExperimentStore} from "../../store/experimentStore";

export default function DocumentUpload(){
    const [file, setFile] = useState(null);
    const setDocumentText = useExperimentStore((state)=>state.setDocumentText);
    const handleFileChange = (e)=>{
        setFile(e.target.files[0]);
    };
    const handleUpload = async ()=>{
        if(!file) return;
        try{
            const result = await uploadDocument(file);
            setDocumentText(result.extracted_text);
        }catch(e){
            console.error("Upload failed:", e);
        }
    };
    return (
        <div className="document-upload-panel">
            <input
                type="file"
                accept=".pdf,.txt,.docx"
                onChange={handleFileChange}
            />
            <button onClick={handleUpload} disabled={!file}>Upload Document</button>
        </div>
    )
}

