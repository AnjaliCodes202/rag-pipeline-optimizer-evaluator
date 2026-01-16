import apiClient from "./apiclient";

export async function uploadDocument(file){
    const formData = new FormData();
    formData.append("file",file);
    const response = await apiClient.post(
        "/documents/upload",
        formData,
        {
            headers:{
                "Content-Type": "multipart/form-data",
            },
        }
    );
    return response.data;
}