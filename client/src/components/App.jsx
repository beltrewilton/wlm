import React, { useState, useRef, useEffect } from "react"
import { useMicVAD, utils } from "@ricky0123/vad-react"
import { streamWAV } from "../api/requestx"

import '../../css/style.css'


export const App = () => {
  const [audioList, setAudioList] = useState([])
  const [mimicAudio, setMimicAudio] = useState()
  const [conversation, addConversation] = useState([])
  const [voice, setVoice] = useState('vctk_low#p236')

  const vad = useMicVAD({
    onSpeechEnd: (audio) => {
      const wavBuffer = utils.encodeWAV(audio)
      const base64 = utils.arrayBufferToBase64(wavBuffer)
      streamWAV(base64, addConversation, setMimicAudio)
      const url = `data:audio/wav;base64,${base64}`
      setAudioList((old) => [url, ...old])
    },
  })

  const OnChangeVoice = (event) => {
    setVoice(event.target.value)
  }

  return (
    <div>
      <div className="head">
        <h1>WLM Demo</h1> 
        {vad.listening && <Raindbow prop={{'userSpeaking': vad.userSpeaking}} /> }
      </div>
     <div className="top">
        <button className="vadbtn" onClick={vad.toggle}>
          {vad.listening && "Listening OFF"}
          {!vad.listening && "listening ON"}
        </button>

       

        <div className="radio-with-Icon">
          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes1" value="vctk_low#p236" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes1">
              <img src="css/woman1.png" className="img-avatar"/><br/>
              vctk_low#p236
            </label>
          </p>

          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes2" value="vctk_low#p239" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes2">
            <img src="css/woman2.png" className="img-avatar"/><br/>
              vctk_low#p239
            </label>
          </p>
          
          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes3" value="vctk_low#p283" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes3">
            <img src="css/woman3.png" className="img-avatar"/><br/>
              vctk_low#p283
            </label>
          </p>

          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes4" value="vctk_low#p330" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes4">
            <img src="css/woman4.png" className="img-avatar"/><br/>
              vctk_low#p330
            </label>
          </p>

          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes5" value="vctk_low#p276" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes5">
            <img src="css/woman5.png" className="img-avatar"/><br/>
              vctk_low#p276
            </label>
          </p>
          
          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes6" value="vctk_low#p286" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes6">
            <img src="css/man1.png" className="img-avatar"/><br/>
              vctk_low#p286
            </label>
          </p>

          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes7" value="cmu-arctic_low#bdl" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes7">
            <img src="css/man2.png" className="img-avatar"/><br/>
             cmu-arctic_low#bdl
            </label>
          </p>

          <p className="radioOption-Item">
            <input type="radio" name="voicesTypes" id="voicesTypes8" value="cmu-arctic_low#ksp" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes8">
            <img src="css/man3.png" className="img-avatar"/><br/>
             cmu-arctic_low#ksp
            </label>
          </p>

        </div>

       
     </div>
      <div className="bl">
        {/* <ol id="playlist">
          {audioList.map((audioURL) => {
            return (
              <li key={audioURL.substring(-10)}>
                <audio className="audio" controls="controls" src={audioURL} />
              </li>
            )
          })}
        </ol> */}

         <ol id="playlist">
          {mimicAudio &&
              <li>
                <audio className="audio" controls="controls"  src={mimicAudio} />
              </li>
          }
        </ol>

        <ol id="conversation">
          {conversation.map((t, i) => {
            return (
              <li key={i} className={t.role}>
                <span className={t.clz}>{t.text}</span>
              </li>
            )
          })}
        </ol>
      </div>
    </div>
  )
}

const Raindbow = (prop) => {
  // console.log('userSpeaking?', prop.prop.userSpeaking)
  const rainbow = useRef()
  const green = useRef()
  const pink = useRef()
  const blue = useRef()
  const [userSpeaking, setUserSpeaking] = useState(false)


  useEffect(() => {
    if (prop.prop.userSpeaking) {
      green.current.classList.add('green')
      pink.current.classList.add('pink')
      blue.current.classList.add('blue')
      rainbow.current.style.setProperty('--rainbow-animation', '0.3s')
    } else {
      green.current.classList.remove('green')
      pink.current.classList.remove('pink')
      blue.current.classList.remove('blue')
      rainbow.current.style.setProperty('--rainbow-animation', '4s')
    }
  }, [prop.prop.userSpeaking])

  return (
    <div ref={rainbow} className="rainbow-container">
      <div ref={green} className=""></div>
      <div ref={pink} className=""></div>
      <div ref={blue} className=""></div>
    </div>
    )
}
