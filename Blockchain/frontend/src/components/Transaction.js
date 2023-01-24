import React from 'react'

export default function Transaction({transaction}) {
  const {input,output}=transaction;
  const recipient=Object.keys(output);
  return (
    <div className='Transaction'>
      <div>From: {input.address}</div>
      {
        recipient.map(recipient=>(
          <div key={recipient}>TO: {recipient} Sent:{output[recipient]}</div>
        ))
      }
    </div>
  )
}
