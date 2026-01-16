//1️⃣ PURPOSE (system terms)
//This store is the single source of truth for the dashboard.
//It:
//holds inputs (document, query, pipelines)
//holds results (run / compare / recommend)
//exposes actions that call backend APIs
//It does not:
//compute scores
//rank pipelines
//interpret results
//Those belong to the backend (already correct).

import {create} from "zustand";
import {runExperiment,comparePipelines,recommendPipeline} from "../services/experimentApi";

export const useExperimentStore = create((set,get)=>({
     documentText: "",
     query: "",
     pipelines: [],
     runResult:null,
     comparisonResults: [],
     recommendation: null,
     loading:false,
     error:null,
     setDocumentText: (text) => set({documentText:text}),
     setQuery: (query) => set({query:query}),
     setPipelines: (pipelines) => set({pipelines:pipelines}),
     runSinglePipeline: async (pipeline) => {
                   set({loading:true, error:null});
                   try{
                       const result = await runExperiment({
                             pipeline_id: pipeline.pipeline_id,
                             query: get().query,
                             document_text: get().documentText,
                             pipeline_config: pipeline.pipeline_config
                       });
                       set({
                           runResult: result,
                           comparisonResults: [],
                           recommendation: null
                       });
                   }catch(err){
                        set({error:err.message || "Run Failed"})
                   }finally{
                        set({loading: false})
                   }
               },
     compareAllPipelines: async () => {
                   set({loading:true, error:null});
                   try{
                       const result = await comparePipelines({
                                query: get().query,
                                document_text:get().documentText,
                                pipelines:get().pipelines
                       });
                       set({
                           comparisonResults:result,
                           runResult:null,
                           recommendation:null
                       });
                   }catch(err){
                       set({error:err.message||"comparison Failed"});
                   }finally{
                       set({loading:false});
                   }
               },
     recommendBestPipeline: async() =>{
                   set({loading:true,error:null})
                   try{
                      const recommendation = await recommendPipeline({
                            query:get().query,
                            document_text:get().documentText,
                            pipelines: get().pipelines
                      });
                      set({
                          recommendation,
                          runResult:null,
                          comparisonResults:[]
                      });
                   }catch(err){
                      set({error:err.message || "Recommendation failed"});

                   }finally{
                      set({loading:false});
                   }
               }
}));