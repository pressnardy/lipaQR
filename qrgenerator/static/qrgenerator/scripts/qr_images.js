async function downloadAllImages(containerSelector) {
  const container = document.querySelector(containerSelector);
  if (!container) {
    console.error("Container not found:", containerSelector);
    return;
  }

  const images = container.querySelectorAll("img");
  if (images.length === 0) {
    console.warn("No images found in container:", containerSelector);
    return;
  }

  for (let i = 0; i < images.length; i++) {
    const img = images[i];
    const imageUrl = img.src;
    if (!imageUrl) continue;

    try {
      const response = await fetch(imageUrl, { mode: "cors" });
      if (!response.ok) throw new Error(`Failed to fetch image: ${imageUrl}`);

      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = blobUrl;

      const urlParts = imageUrl.split("/");
      const filename = urlParts[urlParts.length - 1].split("?")[0] || `image-${i + 1}.jpg`;
      link.download = filename;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // Clean up the blob URL
      URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error("Error downloading image:", imageUrl, error);
    }
  }
}

// const images = document.getElementById('qr-codes-wrapper')

const button = document.getElementById('btn-download')
button.addEventListener('click', ()=> {
    downloadAllImages('#qr-codes-wrapper')
})

