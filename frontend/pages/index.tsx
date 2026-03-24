import React, { useEffect, useRef, useState } from 'react'

export default function Home() {
  const wsRef = useRef<WebSocket | null>(null)
  const [lang, setLang] = useState('en')
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/voice')
    ws.binaryType = 'arraybuffer'
    ws.onopen = () => setConnected(true)
    ws.onmessage = (ev) => {
      // play received audio chunk
      const blob = new Blob([ev.data], { type: 'audio/wav' })
      const url = URL.createObjectURL(blob)
      const a = new Audio(url)
      a.play()
    }
    ws.onclose = () => setConnected(false)
    wsRef.current = ws
    return () => ws.close()
  }, [])

  const startCapture = async () => {
    // placeholder: in production capture microphone, encode and send binary chunks
    if (!wsRef.current) return
    // send a small binary payload to trigger STT stub
    wsRef.current.send(new Uint8Array([1,2,3]))
  }

  return (
    <div style={{padding:20}}>
      <h1>Voice AI Agent (Demo)</h1>
      <p>Connected: {connected ? 'yes' : 'no'}</p>
      <p>Language: {lang}</p>
      <button onClick={startCapture}>Send Test Audio Chunk</button>
    </div>
  )
}
