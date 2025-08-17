document.querySelectorAll('.mark-paid').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        // Find the closest .status ancestor
        const statusDiv = btn.closest('.status');
        if (statusDiv) {
            const infoBox = statusDiv.querySelector('.info-box');
            if (infoBox) {
                infoBox.style.display = 'block';
            }
        }
    });
    btn.addEventListener('mouseleave', function() {
        const statusDiv = btn.closest('.status');
        if (statusDiv) {
            const infoBox = statusDiv.querySelector('.info-box');
            if (infoBox) {
                infoBox.style.display = 'none';
            }
        }
    });
});

function showInfo(targetElement, inforElement){
    
}

