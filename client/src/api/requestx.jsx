import axios from "axios";



export const streamWAV = (wavBuffer, addConversation, setMimicAudio, setStr, __uuid) => {
    let waitaudio;
    const HOST = document.location.href
    // const HOST = 'https://localhost:8770/'
    const msg = {
        'wavBuffer': wavBuffer
    }

    const options_trs = {
        method: 'POST',
        url: `${HOST}core/transcribe_audio/${__uuid}`,
        headers: {
            'Content-Type': 'application/json',
        },
        data: msg,
    }

    const get_options_llama = (trs) => {
        let voice = undefined
        try {
            voice = document.querySelector('input[name="voicesTypes"]:checked').value
        } catch (e) {
            voice =  'vctk_low#p236'
        }

        // console.log(voice)

        const _data = {
            'transcript': trs,
            'voice_base': voice,
        }
        const options_llama = {
            method: 'POST',
            url: `${HOST}core/hit_llama/${__uuid}`,
            headers: {
                'Content-Type': 'application/json',
            },
            data: _data,
        }
        return options_llama
    }

    const pleasewait = () => {
        let voice = undefined
        try {
            voice = document.querySelector('input[name="voicesTypes"]:checked').value
        } catch (e) {
            voice =  'vctk_low#p236'
        }

        console.log(voice)

        const _data = {
            'voice_base': voice,
        }
        const options_dummy = {
            method: 'POST',
            url: `${HOST}core/say_hello`,
            headers: {
                'Content-Type': 'application/json',
            },
            data: _data,
        }
        axios.request(options_dummy).then(function (response) {
            const a = response.data
            const urlx = `data:audio/wav;base64,${a}`
            waitaudio = new Audio(urlx)
            waitaudio.play()
        }).catch(function (error) {
            console.error(error)
        })
    }


    const request_llama = (trs) => {
        setStr('> ')
        document.querySelector('.vadbtn').click()
        // pleasewait()

        axios.request(get_options_llama(trs)).then(function (response) {
            const {text, base64_audio} = response.data
            const url = `data:audio/wav;base64,${base64_audio}`
            setMimicAudio(url)
            const sound = new Audio(url)
            sound.onplay = () => {
                document.querySelector('.bl').style.setProperty('--animate-glow', '0.5s')
                try {
                    waitaudio.pause()
                } catch(e) { }
            }
            sound.onended = () => {
                document.querySelector('.bl').style.setProperty('--animate-glow', '3.5s')
                document.querySelector('.vadbtn').click()
            }

            sound.play()
            
            // addConversation((old) => [{'role': 'llm', 'text': text, 'clz': ''}, ...old])

            // text.choices.forEach(ch => {
            //     addConversation((old) => [{'role': 'llm', 'text': ch.message.content, 'clz': ''}, ...old])
            // })
        }).catch(function (error) {
            console.error(error)
        })
    }

    axios.request(options_trs).then(function (response) {
        const trs = response.data

        addConversation((old) => [...old, {'role': 'human', 'text': trs, 'clz': ''}])
        addConversation((old) => [...old, {'role': 'llm', 'text': '>', 'clz': ''}])
        
        request_llama(trs)
    }).catch(function (error) {
        console.error(error)
    })


}
