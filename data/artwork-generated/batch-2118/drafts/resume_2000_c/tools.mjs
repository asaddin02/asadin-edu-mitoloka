import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import sharp from 'sharp';

export const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
export const write = (p, value) => { fs.mkdirSync(path.dirname(p), {recursive:true}); fs.writeFileSync(p, JSON.stringify(value,null,2)+'\n'); };
export const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
export function copyIndependent(source, destination) {
  fs.mkdirSync(path.dirname(destination), {recursive:true});
  fs.copyFileSync(source, destination+'.new');
  fs.renameSync(destination+'.new', destination);
}
export async function finishCorrection(batch, slug, specPath, generated, notes) {
  const base=`data/artwork-generated/batch-${batch}`;
  const receiptPath=`${base}/${slug}.json`;
  const old=read(receiptPath), spec=read(specPath);
  if(old.status!=='needs-correction') throw new Error(`Concurrent status changed: ${old.status}`);
  let n=1; while(fs.existsSync(`${base}/rejected/${slug}-attempt-${String(n).padStart(2,'0')}.json`)) n++;
  const archive=`${base}/rejected/${slug}-attempt-${String(n).padStart(2,'0')}`;
  if(hash(old.original_file)!==old.native_sha256) throw new Error('Historical hash mismatch');
  copyIndependent(old.original_file,archive+'.png');
  const rejected={original_file:archive+'.png',receipt_file:archive+'.json',native_sha256:old.native_sha256,reason:old.correction_notes};
  write(archive+'.json',{...rejected,prompt:old.prompt,generated_file:old.generated_file,tool:old.tool,image_model:old.image_model,worker_agent:old.worker_agent,basis_claim_ids:old.basis_claim_ids,visual_requirements:old.visual_requirements});
  const target=`${base}/originals/${slug}.png`;
  copyIndependent(generated,target);
  const sha=hash(target), meta=await sharp(target).metadata(), now=new Date().toISOString();
  const receipt={...old,...spec,worker_agent:'resume_2000_c',subagent_model:'gpt-6.1-sol',subagent_reasoning_effort:'high',status:'awaiting-independent-review',tool:'OpenAI built-in image_gen',image_model:'tidak dilaporkan alat',generated_file:generated,generated_at:now,original_file:target,native_sha256:sha,width:meta.width,height:meta.height,rejected_attempts:[...(old.rejected_attempts||[]),...(spec.rejected_attempts||[]),rejected],generation_failures:old.generation_failures||[],visual_review:{reviewer:'codex',verdict:'pass',notes,limitations:[],native_sha256:sha,reviewed_at:now}};
  for(const k of ['root_visual_review','independent_visual_review','correction_notes'])delete receipt[k];
  write(receiptPath,receipt);
  await sharp(target).resize(200,200).png().toFile(`${base}/drafts/resume_2000_c/${slug}-200.png`);
  return receipt;
}

export async function recordReview(batch, slug, notes, pass=true) {
  const base=`data/artwork-generated/batch-${batch}`, r=read(`${base}/${slug}.json`);
  if(hash(r.original_file)!==r.native_sha256)throw new Error('Hash mismatch');
  const p=`${base}/drafts/resume_2000_c/codex-native-reviews.json`, registry=fs.existsSync(p)?read(p):{};
  const thumb=`${base}/drafts/resume_2000_c/${slug}-200.png`;
  await sharp(r.original_file).resize(200,200).png().toFile(thumb);
  registry[slug]={reviewer:'codex',native_reviewed:true,thumbnail_200_reviewed:true,thumbnail_path:thumb,native_sha256:r.native_sha256,verdict:pass?'pass':'reject',sangar_checks:pass?[true,true,true,true,true,true,true]:null,notes,reviewed_at:new Date().toISOString()};
  write(p,registry);
  return registry[slug];
}
