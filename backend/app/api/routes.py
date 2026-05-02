from fastapi import APIRouter, Response

router = APIRouter()

@router.get('/health')
def health():
    return {'status': 'ok'}

@router.get('/')
def root():
    return {
        'service': 'Restaurant Ops Dashboard / iiko Collector',
        'status': 'ok',
        'docs': '/docs',
        'health': '/health'
    }

@router.get('/favicon.ico', include_in_schema=False)
def favicon():
    return Response(status_code=204)
