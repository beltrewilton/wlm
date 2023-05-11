import axios from "axios";
import { uuid } from "../util/utils"
import { letme } from "../util/please_wait_base64";


export const streamwav = (wavBuffer, addConversation, setMimicAudio, voice) => {
    const HOST = document.location.href
    const _uuid = uuid()
    const msg = {
        'wavBuffer': wavBuffer
    }

    const options_trs = {
        method: 'POST',
        url: `${HOST}core/transcribe_audio/${_uuid}`,
        headers: {
            'Content-Type': 'application/json',
        },
        data: msg,
    }

    const get_options_llama = (trs) => {
        const _data = {
            'transcript': trs,
            'voice_base': voice,
        }
        const options_llama = {
            method: 'POST',
            url: `${HOST}core/hit_llama/${_uuid}`,
            headers: {
                'Content-Type': 'application/json',
            },
            data: _data,
        }
        return options_llama
    }


    const request_llama = (trs) => {
        const urlx = `data:audio/wav;base64,${letme}`
        const waitaudio = new Audio(urlx)
        waitaudio.play()

        axios.request(get_options_llama(trs)).then(function (response) {
            const {text, base64_audio} = response.data
            const url = `data:audio/wav;base64,${base64_audio}`
            setMimicAudio(url)
            const sound = new Audio(url)
            sound.onplay = () => {
                document.querySelector('.bl').style.setProperty('--animate-glow', '0.5s')
                waitaudio.pause()
            }
            sound.onended = () => {
                document.querySelector('.bl').style.setProperty('--animate-glow', '3.5s')
            }

            sound.play()

            text.choices.forEach(ch => {
                addConversation((old) => [{'role': 'llm', 'text': ch.text, 'clz': ''}, ...old])
            })
        }).catch(function (error) {
            console.error(error);
        })
    }

    axios.request(options_trs).then(function (response) {
        const trs = response.data
        addConversation((old) => [{'role': 'human', 'text': trs, 'clz': ''}, ...old])
        request_llama(trs)
    }).catch(function (error) {
        console.error(error);
    })


}
