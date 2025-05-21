document.addEventListener('DOMContentLoaded', function () {
  const fileInput = document.getElementById('image');
  const captureBtn = document.getElementById('captureBtn');
  const processBtn = document.getElementById('processBtn');
  const saveImageBtn = document.getElementById('saveImageBtn');
  const resetBtn = document.getElementById('resetBtn');

  const processTypeInput = document.getElementById('process_type');
  const transformTypeInput = document.getElementById('transform_type');

  const cameraContainer = document.getElementById('cameraContainer');
  const cameraPreview = document.getElementById('cameraPreview');
  const captureImageBtn = document.getElementById('captureImageBtn');
  const closeCameraBtn = document.getElementById('closeCameraBtn');
  const cameraCanvas = document.getElementById('cameraCanvas');
  const inputImage = document.getElementById('inputImage');
  const outputImage = document.getElementById('outputImage');

  // Event listener untuk memilih gambar dari file input
  fileInput.addEventListener('change', function () {
    displayImage(fileInput.files[0]);
  });

  // Event listener untuk tombol Capture Gambar dengan Kamera
  captureBtn.addEventListener('click', function () {
    startCamera();
    cameraContainer.style.display = 'block'; // Menampilkan elemen kamera
  });

  // Menyalakan kamera dan menampilkan stream video
  function startCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
          cameraPreview.srcObject = stream;
        })
        .catch(function (error) {
          alert('Tidak dapat mengakses kamera: ' + error.message);
        });
    } else {
      alert('API kamera tidak didukung oleh browser ini.');
    }
  }

  // Menangkap gambar dari video stream
  captureImageBtn.addEventListener('click', function () {
    const context = cameraCanvas.getContext('2d');
    cameraCanvas.width = cameraPreview.videoWidth;
    cameraCanvas.height = cameraPreview.videoHeight;
    context.drawImage(cameraPreview, 0, 0, cameraCanvas.width, cameraCanvas.height);
    const imageData = cameraCanvas.toDataURL('image/png'); // Convert ke base64
    inputImage.src = imageData; // Menampilkan gambar pada halaman

    // Menyembunyikan kamera setelah gambar diambil
    cameraContainer.style.display = 'none';
    stopCamera();
  });

  // Menutup kamera tanpa mengambil gambar
  closeCameraBtn.addEventListener('click', function () {
    cameraContainer.style.display = 'none';
    stopCamera();
  });

  // Fungsi untuk menghentikan kamera
  function stopCamera() {
    const stream = cameraPreview.srcObject;
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach(function (track) {
        track.stop();
      });
      cameraPreview.srcObject = null;
    }
  }

  // Fungsi untuk menampilkan gambar yang di-upload oleh pengguna
  function displayImage(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const imgElement = document.getElementById('inputImage');
      imgElement.src = e.target.result;
      document.getElementById('emptyState').style.display = 'none';
      document.getElementById('imageResults').style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  // Proses pengolahan gambar (tombol proses gambar)
  processBtn.addEventListener('click', function () {
    const formData = new FormData();
    let file = fileInput.files[0];

    // Jika gambar diambil dari kamera, gunakan base64 dari canvas
    if (inputImage.src.startsWith('data:image/png;base64,')) {
      file = dataURLtoFile(inputImage.src, 'captured_image.png');
    }

    if (!file) {
      alert('Silakan pilih gambar terlebih dahulu.');
      return;
    }

    formData.append('image', file);
    formData.append('process_type', processTypeInput.value); // pastikan value yang dipilih dari dropdown terambil dengan benar

    fetch('/process', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.blob())
      .then((blob) => {
        outputImage.src = URL.createObjectURL(blob);
      })
      .catch((error) => {
        console.error('Terjadi kesalahan saat memproses citra:', error);
      });
  });

  // Fungsi untuk mengonversi data URL ke file
  function dataURLtoFile(dataURL, filename) {
    const arr = dataURL.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
  }

  // Menangani reset gambar (kembalikan ke keadaan semula)
  resetBtn.addEventListener('click', function () {
    document.getElementById('image').value = '';
    document.getElementById('emptyState').style.display = 'flex';
    document.getElementById('imageResults').style.display = 'none';
  });

  // Menangani penyimpanan citra hasil pemrosesan
  saveImageBtn.addEventListener('click', function () {
    const imgElement = document.getElementById('outputImage');
    const link = document.createElement('a');
    link.href = imgElement.src;
    link.download = 'processed_image.png';
    link.click();
  });
});
