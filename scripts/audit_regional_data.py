import pandas as pd
import json
from pathlib import Path
root=Path('data/regional-2021')
plays=pd.read_csv(root/'plays.csv').set_index(['gameId','playId'])
total_rows=0
usable=set()
examples=[]
for i,path in enumerate(sorted((root/'tracking').glob('*.csv'))):
 df=pd.read_csv(path,usecols=['gameId','playId','frameId','nflId','team','x','y','event'])
 total_rows+=len(df)
 snaps=df[df.event.eq('ball_snap')].groupby(['gameId','playId']).frameId.min().rename('snapFrame')
 df=df.join(snaps,on=['gameId','playId'])
 pre=df[df.frameId.lt(df.snapFrame) & df.nflId.notna() & df.x.notna() & df.y.notna()]
 counts=pre.groupby(['gameId','playId','frameId']).agg(n=('nflId','size'),unique=('nflId','nunique'),teams=('team','nunique'))
 complete=counts[(counts.n.eq(22)) & (counts.unique.eq(22)) & (counts.teams.eq(2))]
 for key in complete.reset_index().groupby(['gameId','playId']).frameId.max().items():
  (game,play),frame=key
  if (game,play) not in plays.index:continue
  metadata=plays.loc[(game,play)]
  if pd.isna(metadata.pff_passCoverage):continue
  rows=pre[(pre.gameId.eq(game)) & pre.playId.eq(play) & pre.frameId.eq(frame)]
  if sorted(rows.groupby('team').size().tolist())!=[11,11]:continue
  usable.add((int(game),int(play)))
  if len(examples)<3 and metadata.pff_passCoverage not in [x['label'] for x in examples]:
   examples.append({'gameId':int(game),'playId':int(play),'frameId':int(frame),'label':metadata.pff_passCoverage,'down':int(metadata.down),'yardsToGo':int(metadata.yardsToGo),'players':rows[['nflId','team','x','y']].to_dict('records')})
 if (i+1)%20==0:print(i+1,'files audited',flush=True)
result={'tracking_files':i+1,'tracking_rows':total_rows,'raw_plays':len(plays),'usable_pre_snap_plays':len(usable),'classes':plays.pff_passCoverage.value_counts().to_dict(),'examples':examples}
(root/'audit.json').write_text(json.dumps(result,indent=2))
print({k:v for k,v in result.items() if k not in ['examples','classes']},flush=True)
