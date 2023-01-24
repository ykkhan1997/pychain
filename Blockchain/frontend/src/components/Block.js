import React, { useState } from 'react'
import { MILLISECONDS_PY } from '../config';
import Transaction from './Transaction';
import {Button} from 'react-bootstrap';
function ToogleDisplayTransaction({block}){
    const [transactionDisplay,setTransactionDisplay]=useState(false);
    const toogleTransactionDisplay=()=>{
        setTransactionDisplay(!transactionDisplay);
    }
    const {data}=block;
    if (transactionDisplay){
        return(
        <div>
            {
                data.map(transaction=>(
                    <div key={transaction.id}><Transaction transaction={transaction}/></div>
                ))
            }
            <br/>
            <Button variant='danger'size='sm'onClick={toogleTransactionDisplay}>Show Less</Button>
        </div>
        )
    }
    return(
        <div><Button variant='danger'size='sm'onClick={toogleTransactionDisplay}>Show More</Button></div>
    )
}
export default function Block({block}) {
    const {timestamp,hash}=block;
    const timestampDisplay=new Date(timestamp/MILLISECONDS_PY).toLocaleString()
    const hashDisplay=`${hash.substring(0,15)}....`
  return (
    <div className='Block'>
        <div>{timestampDisplay}</div>
        <div>{hashDisplay}</div>
        <br/>
        <ToogleDisplayTransaction block={block}/>
    </div>
  )
}
