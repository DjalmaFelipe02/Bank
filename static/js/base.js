const body = document.querySelector('body'),
         sidebar = body.querySelector('nav'),
         toggle = body.querySelector(".toggle"),
         searchBtn = body.querySelector(".search-box"),
         modeSwitch = body.querySelector(".toggle-switch"),
         modeText = body.querySelector(".mode-text");
   
         // Função para atualizar o texto do modo
         const updateModeText = () => {
            if(body.classList.contains("dark")){
                modeText.innerText = "Dark Mode";
            }  {
                modeText.innerText = "Light mode";
            }
          };
   
           // Atualiza o texto do modo na inicialização
          updateModeText();
   
   
          toggle.addEventListener("click" , () =>{
              sidebar.classList.toggle("close");
          })
          
          searchBtn.addEventListener("click" , () =>{
              sidebar.classList.remove("close");
          })
          
          modeSwitch.addEventListener("click" , () =>{
              body.classList.toggle("dark");
              
          });