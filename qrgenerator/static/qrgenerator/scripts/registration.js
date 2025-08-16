
const eyeOpenSvg = `
    <svg id="eye-open" color="gray.100" fill="currentColor" height="22" viewBox="0 0 22 22" width="22" 
    xmlns="http://www.w3.org/2000/svg" sx="[object Object]" class="css-gy660l">
    <path d="M10.998 14a3 3 0 100-6 3 3 0 000 6z"></path>
    <path clip-rule="evenodd" d="M1 10.184v-.002l.019-.04a4.533 4.533 0 01.148-.294 
    9.87 9.87 0 01.418-.712c.367-.57.927-1.323 1.712-2.078C4.885 5.531 7.403 4 10.997 
    4c3.595 0 6.113 1.531 7.701 3.058a11.664 11.664 0 011.712 2.078 9.894 9.894 0 
    01.532.935l.034.072.012.025.004.01.002.004.001.002v.315L21 10.5l-.003 
    1v.316l-.002.002-.002.004-.004.01-.012.025-.034.072a9.89 9.89 0 
    01-.532.934c-.367.571-.927 1.324-1.712 2.079C17.11 16.469 14.592 18 
    10.998 18c-3.595 0-6.113-1.531-7.701-3.058a11.662 11.662 0 01-1.712-2.078 
    9.866 9.866 0 01-.532-.935 4.533 4.533 0 01-.034-.072l-.012-.025-.004-.01L1 
    11.818 1 11.816v-1.632zM10.998 6c-5.943 0-8.172 5-8.172 5s2.229 5 8.171 5c5.944 0 
    8.172-5 8.172-5s-2.229-5-8.171-5z" fill-rule="evenodd"></path>
    </svg>
`

const eyeClosedSvg = `
    <svg color="gray.100" id="eye-closed" fill="currentColor" height="22" viewBox="0 0 22 22" width="22" xmlns="http://www.w3.org/2000/svg" sx="[object Object]" class="css-gy660l"><path clip-rule="evenodd" d="M15 2h2L7 20H5l1.593-2.87a10.926 10.926 0 01-3.296-2.188 11.662 11.662 0 01-1.712-2.078 9.866 9.866 0 01-.532-.935 4.533 4.533 0 01-.034-.072l-.012-.025-.004-.01L1 11.816v-1.634l.003-.004.004-.01.012-.025a4.533 4.533 0 01.148-.295 9.87 9.87 0 01.418-.712c.367-.57.927-1.323 1.712-2.078C4.885 5.531 7.403 4 10.997 4c.986 0 1.89.115 2.717.314L14.999 2zM2.825 11s2.229-5 8.171-5c.605 0 1.17.052 1.7.145l-1.068 1.922a3 3 0 00-2.788 5.019L7.57 15.37C4.176 14.026 2.827 11 2.827 11z" fill-rule="evenodd"></path><path d="M10.127 17.97l1.096-1.972C16.997 15.874 19.169 11 19.169 11s-.93-2.086-3.19-3.564l.973-1.751c.674.428 1.255.9 1.746 1.373a11.664 11.664 0 011.712 2.078 9.894 9.894 0 01.532.935l.034.072.012.025.004.01.002.004.001.002v.315L21 10.5v1l-.003.001v.315l-.002.002-.002.004-.004.01-.012.025-.034.072a9.89 9.89 0 01-.532.934c-.367.571-.927 1.324-1.712 2.079C17.11 16.469 14.592 18 10.998 18c-.298 0-.588-.01-.87-.03z"></path></svg>
`

const viewPassword = document.getElementById('eye-wrapper')
if (viewPassword) {
    viewPassword.innerHTML = eyeOpenSvg

    viewPassword.addEventListener('click', ()=> {
        const svgContainer = document.getElementById('eye-wrapper')
        const svg = svgContainer.querySelector('svg')
        const svgId = svg.id
        const password = document.getElementById('password')
        
        if (svgId === 'eye-closed'){
            svgContainer.innerHTML = eyeOpenSvg
            password.type = 'password'
        }
        if (svgId === 'eye-open') {
            svgContainer.innerHTML = eyeClosedSvg
            password.type = 'text'
        }
    });
}
