    // Custom action for scroll animation
    export function scrollTrigger(node) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    node.classList.add('visible');
                }
            });
        }, {
            threshold: 0.15 // Trigger when 15% of element is visible
        });

        observer.observe(node);

        return {
            destroy() {
                observer.disconnect();
            }
        };
    }