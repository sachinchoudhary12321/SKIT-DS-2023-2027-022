const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function uploadCropImage(file: File) {
  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(`${API_BASE_URL}/predictions`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload crop image.");
  }

  return response.json();
}

export async function getPrediction(predictionId: string) {
  const response = await fetch(
    `${API_BASE_URL}/predictions/${predictionId}`
  );

  if (!response.ok) {
    throw new Error("Failed to get prediction status.");
  }

  return response.json();
}

export async function checkBackendHealth(): Promise<{ status: string; healthy: boolean }> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      cache: "no-store",
    });
    if (!response.ok) {
      return { status: "offline", healthy: false };
    }
    const data = await response.json();
    return { status: data.status || "ok", healthy: true };
  } catch {
    return { status: "offline", healthy: false };
  }
}
