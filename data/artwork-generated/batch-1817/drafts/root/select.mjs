import fs from 'node:fs';
import {isDeepStrictEqual} from 'node:util';
import {computeFillStatus} from '../../../../../scripts/gemini/fill-lib.mjs';
const base='data/artwork-generated/batch-1817/drafts/root';
const {status,entries}=await computeFillStatus(JSON.parse(fs.readFileSync('data/creatures.json')));
const manifest=JSON.parse(fs.readFileSync('assets/art/verified-manifest.json'));
const exclusions=JSON.parse(fs.readFileSync('data/artwork-exclusions.json')).items;
const ledgerFiles=fs.readdirSync('data').filter(n=>/^artwork-batch-\d+\.json$/.test(n));
const seen=new Set();for(const f of ledgerFiles){const l=JSON.parse(fs.readFileSync('data/'+f));for(const i of l.items||[])seen.add(i.slug)}
const old=JSON.parse(fs.readFileSync('data/artwork-batch-1617.json'));
const big=['ahura-mazda','sekhmet','tengri','ennead','tammuz','anahita','manat','inari'];
const bigAudit=big.map(slug=>{const prior=old.items.find(i=>i.slug===slug);return {slug,claims_unchanged:isDeepStrictEqual(prior?.research?.claims,entries.get(slug)?.claims),prior_receipt:`data/artwork-generated/batch-1617/${slug}.json`}});
fs.writeFileSync(base+'/big-declines-audit.json',JSON.stringify(bigAudit,null,2)+'\n');
const eligible=Object.entries(status).filter(([s,v])=>v.status==='lengkap-informasi'&&entries.has(s)&&!seen.has(s)&&!manifest.artworks[s]&&!exclusions[s]).map(([s])=>s);
fs.writeFileSync(base+'/eligible-slugs.txt',eligible.join(',')+'\n');
fs.writeFileSync(base+'/selection-session.json',JSON.stringify({selected_at:new Date().toISOString(),eligible_count:eligible.length,excluded_prior_slugs:seen.size,big_declines:bigAudit,rule:'Prior ledger slugs excluded to avoid duplicate pending images or repeated declines; prepare script selects first50 by documented appearance from complete valid research.'},null,2)+'\n');
console.log(JSON.stringify({eligible:eligible.length,bigAudit},null,2));
