// video-player.js
class CustomVideoPlayer {
    constructor(containerId, videoUrl) {
        this.container = document.getElementById(containerId);
        this.videoUrl = videoUrl;
        this.initPlayer();
    }

    initPlayer() {
        // Create video element
        this.videoElement = document.createElement('video');
        this.videoElement.id = 'videoPlayer';
        this.videoElement.controls = true;
        this.videoElement.width = 600;

        // Set the video source
        const source = document.createElement('source');
        source.src = this.videoUrl;
        source.type = 'video/mp4';
        this.videoElement.appendChild(source);

        // Add video element to container
        this.container.appendChild(this.videoElement);

        // Initialize event listeners
        this.initEvents();
    }

    initEvents() {
        this.videoElement.addEventListener('play', () => this.triggerEvent('onPlay'));
        this.videoElement.addEventListener('pause', () => this.triggerEvent('onPause'));
        this.videoElement.addEventListener('ended', () => this.triggerEvent('onEnd'));
    }

    triggerEvent(eventName) {
        const event = new CustomEvent(eventName);
        document.dispatchEvent(event);
    }

    play() {
        this.videoElement.play();
    }

    pause() {
        this.videoElement.pause();
    }

    stop() {
        this.videoElement.pause();
        this.videoElement.currentTime = 0;
    }

    mute() {
        this.videoElement.muted = !this.videoElement.muted;
    }

    setVolume(volume) {
        this.videoElement.volume = volume;
    }

    // Add more methods as needed
}
