const Streamlit = window.Streamlit

Streamlit.init = function() {
    Streamlit.setComponentReady()
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, event => {
        const data = event.detail
        Streamlit.setComponentValue(data)
    })
}

Streamlit.onRender = function() {
    Streamlit.setFrameHeight()
}