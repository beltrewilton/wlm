import React, { useState, useRef, useEffect } from "react"
import { useMicVAD, utils } from "@ricky0123/vad-react"
import { streamWAV } from "../api/requestx"
import { uuid } from "../util/utils"

import '../../css/style.css'


export const App = () => {
  const [audioList, setAudioList] = useState([])
  const [mimicAudio, setMimicAudio] = useState()
  const [conversation, addConversation] = useState([])
  const [str, setStr] = useState('')
  const [voice, setVoice] = useState('vctk_low#p236')
  const __uuid = uuid()

  const vad = useMicVAD({
    onSpeechEnd: (audio) => {
      const wavBuffer = utils.encodeWAV(audio)
      const base64 = utils.arrayBufferToBase64(wavBuffer)
      streamWAV(base64, addConversation, setMimicAudio, setStr, __uuid)
      const url = `data:audio/wav;base64,${base64}`
      setAudioList((old) => [url, ...old])
    },
  })

  useEffect(() => {
    let __text = undefined
    const idxs = []
    var ws = new WebSocket(`wss://localhost:8770/core/ws/${__uuid}`)
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data)
        if (data.sharable != undefined) {
          const chr = data.sharable.chr
          const id  = data.sharable.id
          if (idxs.length == 1) {
            if (idxs[0] != id) {
              __text = undefined
            }
            idxs.pop()
          }
          idxs.push(id)
          __text = __text === undefined ? chr : __text + chr
          setStr(__text)
        } else {
          // the-Welcome
          console.log(data)
        }
    }
  }, [])

  useEffect(() => {
    if (conversation != null && conversation.length > 0) {
      const __conversation = [...conversation]
      const tmp = __conversation.filter(c => c.role == "llm")
      tmp[tmp.length - 1].text = str
      addConversation(__conversation)

      const conv = document.querySelector('#conversation')
      const bl = document.querySelector('.bl')
      conv.scroll({ top: 1500, behavior: 'smooth' })
    }
  }, [str])

  const showVoices = (event) => {
    document.querySelector('.radio-with-Icon').classList.toggle('display-voices')
    document.querySelector('.voices').classList.toggle('display-voices')
    if (event.currentTarget.id != null && event.currentTarget.id != '') {
      const img = document.querySelector(`label[for="${event.currentTarget.id}"] img`).src
      document.querySelector('.display-selected').src = img
    }
  }

  return (
    <div>
      <div className="head">
        <h1>WLM Demo</h1> 
        {vad.listening && <Raindbow prop={{'userSpeaking': vad.userSpeaking}} /> }
      </div>
     <div className="top">
        <button className="vadbtn" onClick={vad.toggle}>
          {vad.listening && <img src="css/img/microphone.png" className="img-avatar"/>}
          {!vad.listening && <img src="css/img/mute.png" className="img-avatar"/>}
        </button>

        <button className="voices" onClick={showVoices}>
          <img src="css/img/woman1.png" className="img-avatar display-selected"/>
        </button>

       

        <div className="radio-with-Icon display-voices" >
          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes1" value="vctk_low#p236" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes1">
              <img src="css/img/woman1.png" className="img-avatar"/><br/>
              vctk_low#p236
            </label>
          </p>

          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes2" value="vctk_low#p239" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes2">
            <img src="css/img/woman2.png" className="img-avatar"/><br/>
              vctk_low#p239
            </label>
          </p>
          
          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes3" value="vctk_low#p283" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes3">
            <img src="css/img/woman3.png" className="img-avatar"/><br/>
              vctk_low#p283
            </label>
          </p>

          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes4" value="vctk_low#p330" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes4">
            <img src="css/img/woman4.png" className="img-avatar"/><br/>
              vctk_low#p330
            </label>
          </p>

          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes5" value="vctk_low#p276" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes5">
            <img src="css/img/woman5.png" className="img-avatar"/><br/>
              vctk_low#p276
            </label>
          </p>
          
          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes6" value="vctk_low#p286" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes6">
            <img src="css/img/man1.png" className="img-avatar"/><br/>
              vctk_low#p286
            </label>
          </p>

          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes7" value="cmu-arctic_low#bdl" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes7">
            <img src="css/img/man2.png" className="img-avatar"/><br/>
             cmu-arctic_low#bdl
            </label>
          </p>

          <p className="radioOption-Item">
            <input onClick={showVoices} type="radio" name="voicesTypes" id="voicesTypes8" value="cmu-arctic_low#ksp" className="select-voice ng-valid ng-dirty ng-touched ng-empty" aria-invalid="false"  />
            <label for="voicesTypes8">
            <img src="css/img/man3.png" className="img-avatar"/><br/>
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

        {/* <ol id="conversation">
          {conversation && (
              <li  className={conversation.role}>
                <span className={conversation.clz}>{conversation.text}</span>
              </li>
          )}
        </ol> */}

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
