import React, { useEffect, useState } from 'react'
import { Button } from 'react-bootstrap';
import { API_BASE_URL } from '../config';
import Block from './Block';
import { Link } from 'react-router-dom';
const PAGE_RANGE=3;
export default function Blockchain() {
  const [blockchain,setBlockchain]=useState([]);
  const [blockchainLength,setBlockchainLength]=useState(0);
  const fetchBlockchainPage=({start,end})=>{
    fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
    .then(response=>response.json())
    .then(json=>setBlockchain(json))
  }
  useEffect(()=>{
    fetchBlockchainPage({start:0,end:PAGE_RANGE})
    fetch(`${API_BASE_URL}/blockchain/length`)
    .then(response=>response.json())
    .then(json=>setBlockchainLength(json));
  },[]);

  const buttonNumber=[];
  for (let i=0;i<blockchainLength/PAGE_RANGE;i++)
  buttonNumber.push(i);
  return (
    <div className='Blockchain'>
      <h3>Blockchain</h3>
      <Link to='/'>Home</Link>
      {
        blockchain.map(block=><Block key={block.hash}block={block}/>)
      }
      <div>
        {
          buttonNumber.map(number=>{
            const start=number*PAGE_RANGE;
            const end=(number+1)*PAGE_RANGE;
            return(
              <span key={number} onClick={()=>fetchBlockchainPage({start,end})}><Button size='sm'variant='danger'>{number+1}</Button>{' '}</span>
            )
          })
        }
      </div>
    </div>
  )
}
