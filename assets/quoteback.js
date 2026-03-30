var editSVG = `<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M3.42852 8.1826L3.83008 6.04181C3.84249 5.9758 3.87452 5.91507 3.92201 5.86756L9.55515 0.234417C9.97431 -0.184732 10.7881 -0.0275712 11.408 0.592253C12.0277 1.21199 12.1848 2.02581 11.7657 2.44496L6.13255 8.0781C6.08504 8.12559 6.02431 8.15763 5.9583 8.17004L3.81761 8.5717C3.76434 8.58168 3.70943 8.57853 3.65765 8.56251C3.60587 8.54649 3.55878 8.51809 3.52045 8.47976C3.48212 8.44143 3.45372 8.39434 3.4377 8.34256C3.42168 8.29078 3.41853 8.23588 3.42852 8.1826ZM10.0266 0.705828L4.46633 6.26605L4.17359 7.82661L5.73407 7.53378L11.2943 1.97355C11.4042 1.86366 11.3175 1.44465 10.9365 1.06366C10.5555 0.682577 10.1364 0.59594 10.0266 0.705828ZM10.2326 12H0.333333C0.289558 12 0.246212 11.9914 0.205768 11.9746C0.165325 11.9579 0.128577 11.9333 0.0976236 11.9024C0.0666701 11.8714 0.0421171 11.8347 0.0253667 11.7942C0.00861633 11.7538 -3.32535e-06 11.7104 9.62344e-10 11.6667V1.76752C-3.32535e-06 1.72374 0.00861633 1.68039 0.0253667 1.63995C0.0421171 1.59951 0.0666701 1.56276 0.0976236 1.53181C0.128577 1.50085 0.165325 1.4763 0.205768 1.45955C0.246212 1.4428 0.289558 1.43418 0.333333 1.43418H5.7154L5.04872 2.10085H0.666667V11.3333H9.89922V6.95119L10.5659 6.28453V11.6667C10.5659 11.7104 10.5573 11.7538 10.5405 11.7942C10.5238 11.8347 10.4992 11.8714 10.4683 11.9024C10.4373 11.9333 10.4006 11.9579 10.3601 11.9746C10.3197 11.9914 10.2763 12 10.2326 12Z" fill="#9DB8BF"/></svg>`
var quoteStyle = `
  @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=Space+Grotesk:wght@700&display=swap');

  .quoteback-container {
    --surface:         #f9f9f7;
    --surface-dim:     #dadad8;
    --surface-low:     #f4f4f2;
    --surface-lowest:  #ffffff;
    --primary:         #000000;
    --primary-fixed:   #5f5e5e;
    --outline:         #777777;
    --on-surface:      #1a1a1a;

    text-rendering: optimizeLegibility;
    background: var(--surface-lowest);
    /* Ghost Border fallback — contrast ratio fails against surface background */
    border: 1px solid #c6c6c6;
    border-radius: 0;
    margin-bottom: 2rem;
    max-width: 800px;
    text-align: left;
    /* Paper block — ambient desk shadow, warm tone */
    box-shadow: 0 2px 32px rgba(26,26,26,0.07);
  }

  /* No hover transform — this is not a SaaS card */
  .quoteback-container:hover {
    transform: none;
    box-shadow: 0 2px 32px rgba(26,26,26,0.07);
    border: 1px solid #c6c6c6;
  }

  .quoteback-parent {
    overflow: hidden;
    position: relative;
    width: 100%;
    box-sizing: border-box;
  }

  .quoteback-content {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 1rem;
    font-style: italic;
    font-weight: 400;
    padding: 2rem;
    color: var(--on-surface);
    line-height: 1.75;
  }

  /* Tonal carving — no border-top */
  .quoteback-head {
    background: var(--surface-low);
    display: flex;
    flex-flow: row nowrap;
    justify-content: start;
    align-items: stretch;
    padding-left: 1.25rem;
  }

  /* Square favicon — 0px radius, no border */
  .quoteback-avatar {
    border-radius: 0;
    border: none;
    width: 36px;
    height: 36px;
    min-width: 36px !important;
    margin: 0.85rem 0;
    position: relative;
    background: var(--surface-dim);
  }

  .quoteback-avatar .mini-favicon {
    width: 20px;
    height: 20px;
    position: absolute;
    margin: auto;
    top: 0; left: 0; right: 0; bottom: 0;
  }

  .quoteback-metadata {
    min-width: 0;
    display: flex;
    flex-shrink: 1;
    align-items: center;
    margin-left: 0.75rem;
  }

  .metadata-inner {
    line-height: 1.3;
    width: 100%;
    max-width: 525px;
  }

  @media (max-width: 414px) {
    .metadata-inner { max-width: 200px; }
  }

  .quoteback-author {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--primary);
    margin-bottom: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .quoteback-title {
    font-family: 'Newsreader', Georgia, serif;
    font-variant-caps: all-small-caps;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    color: var(--outline);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 1.25rem;
  }

  /* Tonal carving instead of border-left */
  .quoteback-backlink {
    margin-left: auto;
    display: flex;
    flex-shrink: 1;
    align-items: center;
    width: 81px;
    min-width: 81px !important;
    padding: 0 1rem !important;
    background: var(--surface-dim);
  }

  .quoteback-arrow {
    border: none !important;
    font-family: 'Newsreader', Georgia, serif !important;
    font-variant-caps: all-small-caps;
    font-size: 0.72rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.06em;
    color: var(--outline) !important;
    text-decoration: none !important;
    transition: color 0.1s ease;
  }

  .quoteback-arrow:hover  { color: var(--primary) !important; }
  .quoteback-arrow:visited { text-decoration: none !important; }

  .editable:focus { outline: none; }
  .editable:before { margin-right: 8px; content: url(data:image/svg+xml,${encodeURIComponent(editSVG)}); }

  .quoteback-content a { color: var(--on-surface); transition: opacity 0.2s ease; }
  .quoteback-content a:hover { opacity: 0.5; }
  .quoteback-content p { margin-block-start: 0; margin-block-end: 0.5em; }
  .quoteback-content p:last-of-type { margin-block-end: 0; }
  .quoteback-content img { width: 100%; height: auto; margin: 0.5em 0; }
  .quoteback-content blockquote {
    border-left: 2px solid var(--outline);
    padding-left: 0.75em;
    margin-inline-start: 1em;
    color: var(--outline);
  }
  .quoteback-content ol,
  .quoteback-content ul { margin-block-start: 0.5em; margin-block-end: 0.5em; }
  .quoteback-content h1,
  .quoteback-content h2,
  .quoteback-content h3 { margin-block-start: 0.5em; margin-block-end: 0.5em; }
`

document.addEventListener("DOMContentLoaded", function(){
    
    // get all our classed blockquote components
    var index = document.querySelectorAll(".quoteback");


    for(var item=0; item < index.length; item++ ){   
      // remove the footer element
      console.log(index[item]);
      index[item].removeChild(index[item].querySelector("footer"));
      
      var text = index[item].innerHTML;

      var url = index[item].cite;
      var author = index[item].getAttribute("data-author");
      var title = index[item].getAttribute("data-title");
      var favicon = `https://s2.googleusercontent.com/s2/favicons?domain_url=${url}&sz=64`
      var darkmode = index[item].getAttribute("darkmode");

      // create a new component with that data
      var component = `
      <quoteback-component darkmode="${darkmode}" url="${url}" text="${encodeURIComponent(text)}" author="${author}" title="${title}" favicon="${favicon}"> 
      </quoteback-component>    
      `;
      var newEl = document.createElement('div');
      newEl.innerHTML = component;
      

      // replace the original blockquote with our quoteback seed component
      index[item].parentNode.replaceChild(newEl, index[item]);

      var template = document.createElement('template');
      template.innerHTML=`
      <style>${quoteStyle}</style>
      <div class="quoteback-container" role="quotation" aria-labelledby="quoteback-author" tabindex="0">
          <div id="quoteback-parent" class="quoteback-parent">
              <div class="quoteback-content"></div>       
          </div>

          <div class="quoteback-head">       
              <div class="quoteback-avatar"><img class="mini-favicon" src=""/></div>     
              <div class="quoteback-metadata">
                  <div class="metadata-inner">
                      <div aria-label="" id="quoteback-author" class="quoteback-author"></div>
                      <div aria-label="" class="quoteback-title"></div>
                  </div>  
              </div>

          <div class="quoteback-backlink"><a target="_blank" aria-label="go to the full text of this quotation" rel="noopener" href="" class="quoteback-arrow">Go to text <span class="right-arrow">&#8594;</span></a></div>
          </div>  
      </div>`;

      class QuoteBack extends HTMLElement {
        constructor(){  
          super();
          this.attachShadow({mode: 'open'});
          this.shadowRoot.appendChild(template.content.cloneNode(true));
  			  
  			  this.text = decodeURIComponent(this.getAttribute('text'));
  			  this.author = this.getAttribute('author');
  			  this.title = decodeURIComponent(this.getAttribute('title')); 
  			  this.url = this.getAttribute('url')
          this.favicon = this.getAttribute('favicon');
          this.editable = this.getAttribute('editable');
          this.darkmode = this.getAttribute('darkmode')

        };
        
        connectedCallback() {
          console.info( 'connected' );

          if(this.darkmode == "true"){
            this.shadowRoot.querySelector('.quoteback-container').classList += " dark-theme";
          }
          this.shadowRoot.querySelector('.quoteback-content').innerHTML = decodeURIComponent(this.getAttribute('text'));
          this.shadowRoot.querySelector('.mini-favicon').src = this.getAttribute('favicon');
          this.shadowRoot.querySelector('.quoteback-author').innerHTML = this.getAttribute('author');
          this.shadowRoot.querySelector('.quoteback-author').setAttribute("aria-label", "quote by " + this.getAttribute('author'));
          this.shadowRoot.querySelector('.quoteback-title').innerHTML = decodeURIComponent(this.getAttribute('title'));
          this.shadowRoot.querySelector('.quoteback-title').setAttribute("aria-label", "title: " + decodeURIComponent(this.getAttribute('title')));
          this.shadowRoot.querySelector('.quoteback-arrow').href = this.getAttribute('url');          

          // Manually focus and blur clicked targets
          // This solves firefox bug where clicking between contenteditable fields doesn't work         
          if(this.editable == "true"){
            let titlediv = this.shadowRoot.querySelector('.quoteback-title');
            let authordiv = this.shadowRoot.querySelector('.quoteback-author');
            
            titlediv.addEventListener("click", evt => {
              evt.target.contentEditable = true;
              evt.target.focus();
            });
            titlediv.addEventListener("blur", evt => {
              evt.target.contentEditable = false;
            });

            authordiv.addEventListener("click", evt => {
              evt.target.contentEditable = true;
              evt.target.focus();
            });
            authordiv.addEventListener("blur", evt => {
              evt.target.contentEditable = false;
            });
          }
          // end this fix

        };                                  

      }

      // if quoteback-component is already defined
      if (customElements.get('quoteback-component')){
          null;
      }else{
          window.customElements.define('quoteback-component', QuoteBack)  
      }
    }
});

// here's some nonsens
