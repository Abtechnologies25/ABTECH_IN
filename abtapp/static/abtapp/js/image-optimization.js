/**
 * Advanced Image Optimization & Lazy Loading
 * Optimizes image loading with blur-up effect and intersection observer
 */

class ImageOptimizer {
    constructor() {
        this.imageSelector = 'img[loading="lazy"]';
        this.observerOptions = {
            rootMargin: '50px',
            threshold: 0.01
        };
        this.init();
    }

    init() {
        // Check if IntersectionObserver is supported
        if ('IntersectionObserver' in window) {
            this.setupIntersectionObserver();
        } else {
            // Fallback for older browsers
            this.loadAllImages();
        }

        // Monitor network conditions
        this.setupNetworkAwareness();
        
        // Handle responsive images
        this.setupResponsiveImages();
    }

    /**
     * Setup Intersection Observer for lazy loading
     */
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, this.observerOptions);

        document.querySelectorAll(this.imageSelector).forEach(img => {
            observer.observe(img);
        });
    }

    /**
     * Load single image with blur-up effect
     */
    loadImage(img) {
        const dataSrc = img.getAttribute('data-src');
        
        if (!dataSrc) {
            img.classList.add('lazy-loaded');
            return;
        }

        // Create a new image for preloading
        const imageLoader = new Image();
        
        imageLoader.onload = () => {
            // Fade in effect
            img.style.transition = 'opacity 0.3s ease-in-out';
            img.src = dataSrc;
            img.removeAttribute('data-src');
            img.classList.add('lazy-loaded');
            
            // Remove blur class if present
            img.classList.remove('lazy-blur');
        };

        imageLoader.onerror = () => {
            console.warn(`Failed to load image: ${dataSrc}`);
            img.classList.add('lazy-error');
        };

        // Start loading
        imageLoader.src = dataSrc;
    }

    /**
     * Fallback for older browsers
     */
    loadAllImages() {
        document.querySelectorAll(this.imageSelector).forEach(img => {
            const dataSrc = img.getAttribute('data-src');
            if (dataSrc) {
                img.src = dataSrc;
                img.removeAttribute('data-src');
            }
        });
    }

    /**
     * Setup network-aware image loading
     * Load lower quality on slow connections
     */
    setupNetworkAwareness() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            
            const handleConnectionChange = () => {
                const effectiveType = connection.effectiveType;
                const quality = this.getImageQualityByConnection(effectiveType);
                document.documentElement.setAttribute('data-connection-quality', quality);
            };

            handleConnectionChange();
            connection.addEventListener('change', handleConnectionChange);
        }
    }

    /**
     * Determine image quality based on connection speed
     */
    getImageQualityByConnection(effectiveType) {
        const qualityMap = {
            '4g': 'high',
            '3g': 'medium',
            '2g': 'low',
            'slow-2g': 'low'
        };
        return qualityMap[effectiveType] || 'medium';
    }

    /**
     * Setup responsive images with picture elements
     */
    setupResponsiveImages() {
        if (!('picture' in document)) {
            // Fallback for browsers without picture element support
            this.setupResponsiveImageFallback();
        }
    }

    /**
     * Fallback for browsers without picture element
     */
    setupResponsiveImageFallback() {
        const observer = new ResizeObserver(() => {
            document.querySelectorAll('picture img').forEach(img => {
                this.updateImageBasedOnSize(img);
            });
        });

        document.querySelectorAll('picture').forEach(picture => {
            observer.observe(picture);
        });
    }

    /**
     * Update image source based on container size
     */
    updateImageBasedOnSize(img) {
        const width = img.parentElement.offsetWidth;
        const srcset = img.getAttribute('srcset');
        
        if (!srcset) return;

        const sources = srcset.split(',').map(s => s.trim());
        let bestSource = sources[0].split(' ')[0];

        sources.forEach(source => {
            const [url, sizeStr] = source.split(' ');
            const size = parseInt(sizeStr);
            
            if (size <= width) {
                bestSource = url;
            }
        });

        if (img.src !== bestSource) {
            img.src = bestSource;
        }
    }

    /**
     * Preload images that are coming up in the viewport
     */
    preloadUpcomingImages(distance = 1000) {
        document.querySelectorAll(this.imageSelector).forEach(img => {
            const rect = img.getBoundingClientRect();
            const distanceFromViewport = rect.top - window.innerHeight;
            
            if (distanceFromViewport < distance && distanceFromViewport > 0) {
                this.loadImage(img);
            }
        });
    }
}

// Gallery Lazy Loading
class GalleryOptimizer extends ImageOptimizer {
    /**
     * Optimize gallery image loading
     */
    setupGalleryLazyLoading() {
        const galleries = document.querySelectorAll('[data-gallery-type]');
        
        galleries.forEach(gallery => {
            const type = gallery.getAttribute('data-gallery-type');
            
            if (type === 'carousel') {
                this.setupCarouselLazyLoading(gallery);
            } else if (type === 'grid') {
                this.setupGridLazyLoading(gallery);
            }
        });
    }

    /**
     * Lazy load for carousels - load next/prev images
     */
    setupCarouselLazyLoading(carousel) {
        const slides = carousel.querySelectorAll('[data-slide]');
        
        const loadAdjacentSlides = (activeIndex) => {
            // Load current slide
            this.loadImage(slides[activeIndex].querySelector('img'));
            
            // Preload next 2 slides
            for (let i = 1; i <= 2; i++) {
                const nextIndex = (activeIndex + i) % slides.length;
                const nextImg = slides[nextIndex].querySelector('img');
                if (nextImg) this.loadImage(nextImg);
            }
        };

        // Monitor carousel navigation
        carousel.addEventListener('slide.bs.carousel', (e) => {
            loadAdjacentSlides(e.to);
        });

        // Load initial slide
        loadAdjacentSlides(0);
    }

    /**
     * Lazy load for grids - prioritize visible images
     */
    setupGridLazyLoading(grid) {
        const images = grid.querySelectorAll('img[loading="lazy"]');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '100px',
            threshold: 0
        });

        images.forEach(img => observer.observe(img));
    }
}

// Performance Monitoring
class ImagePerformanceMonitor {
    /**
     * Monitor image loading performance
     */
    static monitorLoadTime() {
        const images = document.querySelectorAll('img');
        
        images.forEach(img => {
            const startTime = performance.now();
            
            img.addEventListener('load', () => {
                const loadTime = performance.now() - startTime;
                const naturalSize = `${img.naturalWidth}x${img.naturalHeight}`;
                
                console.log(`Image loaded: ${img.src} - Time: ${loadTime.toFixed(2)}ms - Size: ${naturalSize}`);
            });
            
            img.addEventListener('error', () => {
                console.error(`Failed to load image: ${img.src}`);
            });
        });
    }

    /**
     * Report Core Web Vitals
     */
    static reportWebVitals() {
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                list.getEntries().forEach((entry) => {
                    console.log(`${entry.name}: ${entry.duration.toFixed(2)}ms`);
                });
            });

            observer.observe({ entryTypes: ['navigation', 'resource'] });
        }
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize image optimizer
    const optimizer = new ImageOptimizer();
    
    // Initialize gallery optimizer if galleries exist
    if (document.querySelector('[data-gallery-type]')) {
        const galleryOptimizer = new GalleryOptimizer();
        galleryOptimizer.setupGalleryLazyLoading();
    }

    // Monitor performance
    if (window.location.hostname !== 'localhost') {
        ImagePerformanceMonitor.monitorLoadTime();
        ImagePerformanceMonitor.reportWebVitals();
    }

    // Preload upcoming images on scroll
    window.addEventListener('scroll', () => {
        optimizer.preloadUpcomingImages();
    });
});

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ImageOptimizer, GalleryOptimizer, ImagePerformanceMonitor };
}
