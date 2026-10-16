import fs from 'node:fs';
import sharp from 'sharp';
import {read,write,hash,copyIndependent} from '../../../batch-2118/drafts/resume_2000_c/tools.mjs';
export async function finish(slug, generated, notes) {
  const base='data/artwork-generated/batch-2124', spec=read(`${base}/drafts/resume_2000_c/${slug}.json`), batch=read('data/artwork-batch-2124.json');
  const item=batch.items.find(x=>x.slug===slug), target=`${base}/originals/${slug}.png`;
  if(fs.existsSync(`${base}/${slug}.json`))throw new Error('Existing receipt');
  copyIndependent(generated,target);
  const sha=hash(target), meta=await sharp(target).metadata(), now=new Date().toISOString();
  const receipt={...spec,worker:'codex',worker_agent:'resume_2000_c',subagent_model:'gpt-6.1-sol',subagent_reasoning_effort:'high',tool:'OpenAI built-in image_gen',image_model:'tidak dilaporkan alat',status:'awaiting-independent-review',review_path:item.review_path,batch:2124,rationale:batch.user_policy.intent,generated_file:generated,generated_at:now,original_file:target,native_sha256:sha,width:meta.width,height:meta.height,generation_failures:[],rejected_attempts:spec.rejected_attempts||[],visual_review:{reviewer:'codex',verdict:'pass',notes,limitations:[],native_sha256:sha,reviewed_at:now}};
  write(`${base}/${slug}.json`,receipt);
  await sharp(target).resize(200,200).png().toFile(`${base}/drafts/resume_2000_c/${slug}-200.png`);
  return receipt;
}
