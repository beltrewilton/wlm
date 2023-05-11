import React, { useState, useRef, useEffect } from "react"
import { useMicVAD, utils } from "@ricky0123/vad-react"
import { streamwav } from "../api/requestx"

import '../../css/style.css'


export const App = () => {
  const [audioList, setAudioList] = useState([])
  const [mimicAudio, setMimicAudio] = useState()
  const [conversation, addConversation] = useState([])
  const [voice, setVoice] = useState('cmu-arctic_low')

  const vad = useMicVAD({
    onSpeechEnd: (audio) => {
      const wavBuffer = utils.encodeWAV(audio)
      const base64 = utils.arrayBufferToBase64(wavBuffer)
      streamwav(base64, addConversation, setMimicAudio, voice)
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
        
      </div>
     <div className="top">
        <button className="vadbtn" onClick={vad.toggle}>
          {vad.listening && "ON"}
          {!vad.listening && "OFF"}
        </button>
        [Voice]
        <select className="select-voice" onChange={OnChangeVoice}>
              <option value="cmu-arctic_low">cmu-arctic_low</option>
              <option value="vctk_low">vctk_low</option>
              <option value="hifi-tts_low">hifi-tts_low</option>
              <option value="ljspeech_low">ljspeech_low</option>
              <option value="m-ailabs_low">m-ailabs_low</option>
        </select>
        {vad.listening && <Raindbow prop={{'userSpeaking': vad.userSpeaking}} /> }
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

const UserSpeaking = () => {
  return <span style={{ color: "green" }}>user is speaking</span>
}

const UserNotSpeaking = () => {
  return <span style={{ color: "red" }}>user is not speaking</span>
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
