const API_BASE_URL = "http://localhost:5000/api";

const AudioServices = {
  async uploadAudio(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error uploading file:", error);
      throw error;
    }
  },

  async transcribeAudio(filename) {
    console.log("Transcribing audio:", filename);
    try {
      const response = await fetch(`${API_BASE_URL}/transcribe/${filename}`);
      console.log("Response:", response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Transcription response:", data); // Log the response
      return data;
    } catch (error) {
      console.error("Error transcribing audio:", error);
      throw error;
    }
  },

  async summarizeText(text) {
    try {
      const response = await fetch(`${API_BASE_URL}/summarize`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error("Error summarizing text:", error);
      throw error;
    }
  },
};
