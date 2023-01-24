import React,{useState,useEffect} from 'react';
import { Button, FormControl, FormGroup } from 'react-bootstrap';
import { API_BASE_URL } from '../config';
import { Link } from 'react-router-dom';
import history from '../history';
export default function ConductTransaction() {
    const [amount,setAmount]=useState(0);
    const [recipient,setRecipient]=useState('');
    const [knownAddresses,setKnownAddresses]=useState([]);
    useEffect(()=>{
        fetch(`${API_BASE_URL}/known-addresses`)
        .then(response=>response.json())
        .then(json=>setKnownAddresses(json))
    },[]);
    const updateRecipient=event=>{
        setRecipient(event.target.value);
    }
    const updateAmount=event=>{
        setAmount(Number(event.target.value));
    }
    const submitTransaction=()=>{
        fetch(`${API_BASE_URL}/wallet/transact`,
        {
            method:'POST',
            headers:{'Content-Type':'Application/json'},
            body:JSON.stringify({recipient,amount})
        }).then(response=>response.json())
        .then(json=>{
            console.log('submitTransaction json',json);
            alert('Success !');
            history.push('/transaction-pool')
        })
    }
  return (
    <div className='ConductTransaction'>
        <h3>Conduct Transaction</h3>
        <Link to='/'>Home</Link>
        <FormGroup>
            <FormControl inputMode='text'placeholder='recipient'value={recipient}onChange={updateRecipient}/>
        </FormGroup>
        <br/>
        <FormGroup>
            <FormControl inputMode='number'placeholder='Amount'value={amount}onChange={updateAmount}/>
        </FormGroup>
        <div>
            <br/>
            <Button variant='danger'onClick={submitTransaction}>Submit</Button>
        </div>
        <br/>
        <h4>Known Addresses</h4>
        <div>
            {
                knownAddresses.map((knownAddress,i)=>(
                    <span key={knownAddress}><u>{knownAddress}</u>{i!==knownAddresses.length-1?', ':''}</span>
                ))
            }
        </div>
    </div>
  )
}