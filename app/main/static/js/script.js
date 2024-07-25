const btn = document.getElementById('myModal')
// const btn_2 = document.('.model-1')



btn.addEventListener('click',function () {


    
})
function openImage(imageUrl) {
    var fullPageImage = document.createElement('div');
    fullPageImage.classList.add('full-page-image-overlay');
    fullPageImage.innerHTML = '<span class="close-btn" onclick="closeImage()">&times;</span><img src="' + imageUrl + '" class="full-page-image">';
    document.body.appendChild(fullPageImage);
    document.body.style.overflow = 'hidden'; // Prevent scrolling of background content
    
    // Close the full-page image overlay when clicking outside the image
    fullPageImage.addEventListener('click', function(event) {
        if (event.target === fullPageImage) {
            closeImage();
        }
    });
}

function closeImage() {
    var fullPageImage = document.querySelector('.full-page-image-overlay');
    if (fullPageImage) {
        fullPageImage.remove();
        document.body.style.overflow = ''; // Restore scrolling of background content
    }
}



document.addEventListener('DOMContentLoaded', function() {
  const darkModeToggle = document.getElementById('dark-mode-toggle');

  // Function to set the theme based on the checkbox state
  function setTheme(theme) {
      if (theme === 'dark') {
          document.body.classList.add('dark-mode');
      } else {
          document.body.classList.remove('dark-mode');
      }
  }

  // Event listener for checkbox change
  darkModeToggle.addEventListener('change', function() {
      if (this.checked) {
          localStorage.setItem('theme', 'dark');
          setTheme('dark');
      } else {
          localStorage.setItem('theme', 'light');
          setTheme('light');
      }
  });

  // Check the current theme from localStorage
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme) {
      setTheme(currentTheme);
      // Set the checkbox state based on the current theme
      darkModeToggle.checked = currentTheme === 'dark';
  }
});

function toggleVideo(videoId) {
      const videoElement = document.getElementById(videoId);
      const allVideos = document.querySelectorAll('video');

      // Pause and hide all other videos
      allVideos.forEach(video => {
          if (video.id !== videoId) {
              video.pause();
              video.style.display = 'none';
          }
      });

      // Show and play the selected video, or pause and hide if already playing
      if (videoElement.style.display === 'none' || videoElement.paused) {
          videoElement.style.display = 'block';
          videoElement.play();
      } else {
          videoElement.pause();
          videoElement.style.display = 'none';
      }

  }


  document.addEventListener("DOMContentLoaded", function() {
      const videos = document.querySelectorAll('.tweet-video');

      const observer = new IntersectionObserver((entries, observer) => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  entry.target.play();
              } else {
                  entry.target.pause();
              }
          });
      }, {
          threshold: 0.5 // Play the video when 50% of it is visible
      });

      videos.forEach(video => {
          observer.observe(video);
      });
  });
  function openImage(imageUrl) {
    var fullPageImage = document.createElement('div');
    fullPageImage.classList.add('full-page-image-overlay');
    fullPageImage.innerHTML = '<span class="close-btn" onclick="closeImage()">&times;</span><img src="' + imageUrl + '" class="full-page-image">';
    document.body.appendChild(fullPageImage);
    document.body.style.overflow = 'hidden'; // Prevent scrolling of background content
    
    // Close the full-page image overlay when clicking outside the image
    fullPageImage.addEventListener('click', function(event) {
        if (event.target === fullPageImage) {
            closeImage();
        }
    });
}

function closeImage() {
    var fullPageImage = document.querySelector('.full-page-image-overlay');
    if (fullPageImage) {
        fullPageImage.remove();
        document.body.style.overflow = ''; // Restore scrolling of background content
    }
}