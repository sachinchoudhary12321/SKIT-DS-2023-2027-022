/**
 * Client-Side Image Quality & Crop Validation
 * Validates whether an uploaded image contains sufficient visual detail and
 * agricultural foliage, rejecting blank, solid-color, pitch-black, or overexposed images.
 */

export interface ImageValidationResult {
  isValid: boolean;
  error?: string;
  details?: {
    isSolidColor: boolean;
    isTooDark: boolean;
    isTooBright: boolean;
    hasVegetation: boolean;
    stdDev: number;
    meanLuminance: number;
  };
}

export async function validateCropImage(file: File): Promise<ImageValidationResult> {
  return new Promise((resolve) => {
    // Only run in browser environment
    if (typeof window === "undefined" || typeof document === "undefined") {
      resolve({ isValid: true });
      return;
    }

    const img = new Image();
    const objectUrl = URL.createObjectURL(file);
    img.src = objectUrl;

    img.onload = () => {
      URL.revokeObjectURL(objectUrl);

      try {
        const canvas = document.createElement("canvas");
        const size = 64; // 64x64 thumbnail analysis
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext("2d", { willReadFrequently: true });

        if (!ctx) {
          resolve({ isValid: true });
          return;
        }

        ctx.drawImage(img, 0, 0, size, size);
        const imgData = ctx.getImageData(0, 0, size, size);
        const data = imgData.data;
        const totalPixels = size * size;

        let sumLum = 0;
        let sumLumSq = 0;
        let botanicalPixels = 0;

        for (let i = 0; i < data.length; i += 4) {
          const r = data[i];
          const g = data[i + 1];
          const b = data[i + 2];

          // Standard perceived luminance
          const lum = 0.299 * r + 0.587 * g + 0.114 * b;
          sumLum += lum;
          sumLumSq += lum * lum;

          // Botanical / agricultural foliage tones (greens, leaf yellows, diseased rust/blight spots)
          const isGreenFoliage = g > r * 0.92 && g > b * 1.05 && g > 30;
          const isPlantLesion = r > 65 && g > 55 && b < 135 && (r > b || g > b);
          const isHighContrastOrganic = Math.abs(r - g) > 20 || Math.abs(g - b) > 20;

          if (isGreenFoliage || isPlantLesion || isHighContrastOrganic) {
            botanicalPixels++;
          }
        }

        const meanLum = sumLum / totalPixels;
        const variance = (sumLumSq / totalPixels) - (meanLum * meanLum);
        const stdDev = Math.sqrt(Math.max(0, variance));
        const vegetationRatio = botanicalPixels / totalPixels;

        // 1. Pitch black (camera covered or pocket image)
        if (meanLum < 15) {
          resolve({
            isValid: false,
            error: "The image is too dark (pitch black or camera obstructed). Please take a photo with adequate lighting.",
            details: {
              isSolidColor: false,
              isTooDark: true,
              isTooBright: false,
              hasVegetation: false,
              stdDev,
              meanLuminance: meanLum,
            },
          });
          return;
        }

        // 2. Washed out pure white / overexposed
        if (meanLum > 245 && stdDev < 15) {
          resolve({
            isValid: false,
            error: "The image is completely overexposed or pure white. Please take a clear photo of the crop.",
            details: {
              isSolidColor: false,
              isTooDark: false,
              isTooBright: true,
              hasVegetation: false,
              stdDev,
              meanLuminance: meanLum,
            },
          });
          return;
        }

        // 3. Solid color / blank image check (low pixel standard deviation)
        if (stdDev < 12) {
          resolve({
            isValid: false,
            error: "Blank or solid image detected. The image lacks visible crop features or texture. Please upload a clear photo of an actual crop leaf or plant.",
            details: {
              isSolidColor: true,
              isTooDark: meanLum < 20,
              isTooBright: meanLum > 240,
              hasVegetation: false,
              stdDev,
              meanLuminance: meanLum,
            },
          });
          return;
        }

        // 4. Low texture uniform surface (e.g. plain desk, grey card, blank wall)
        if (stdDev < 22 && vegetationRatio < 0.05) {
          resolve({
            isValid: false,
            error: "No crop or foliage detected. Please upload an image focused on the crop or plant leaf.",
            details: {
              isSolidColor: false,
              isTooDark: false,
              isTooBright: false,
              hasVegetation: false,
              stdDev,
              meanLuminance: meanLum,
            },
          });
          return;
        }

        // Valid image
        resolve({
          isValid: true,
          details: {
            isSolidColor: false,
            isTooDark: false,
            isTooBright: false,
            hasVegetation: vegetationRatio > 0.1,
            stdDev,
            meanLuminance: meanLum,
          },
        });
      } catch {
        resolve({ isValid: true });
      }
    };

    img.onerror = () => {
      URL.revokeObjectURL(objectUrl);
      resolve({
        isValid: false,
        error: "Unable to read the image file. Please choose a valid JPG or PNG photo.",
      });
    };
  });
}
