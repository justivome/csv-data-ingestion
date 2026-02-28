<script setup lang="ts">
import { ref } from 'vue'
import { useUploadMutation } from '~/api/datasets'

const emit = defineEmits<{
  uploaded: []
}>()

const router = useRouter()
const fileInput = ref<HTMLInputElement>()
const selectedFile = ref<File | null>(null)
const error = ref('')

const { mutateAsync: upload, isLoading } = useUploadMutation()

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  selectedFile.value = target.files?.[0] ?? null
  error.value = ''
}

async function handleUpload() {
  if (!selectedFile.value) {
    error.value = 'Please select a CSV file'
    return
  }

  error.value = ''
  try {
    const data = await upload(selectedFile.value)
    emit('uploaded')
    router.push(`/datasets/${data.dataset_id}`)
  }
  catch (err: any) {
    error.value = err?.data?.detail || 'Upload failed'
  }
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Upload CSV</CardTitle>
      <CardDescription>Upload a sales CSV file for processing</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="flex gap-4 items-center">
        <Input
          ref="fileInput"
          type="file"
          accept=".csv"
          class="max-w-sm"
          @change="onFileChange"
        />
        <Button :disabled="isLoading" @click="handleUpload">
          <template v-if="isLoading">
            <Icon name="i-lucide:loader-2" class="mr-2 animate-spin" />
            Processing...
          </template>
          <template v-else>
            <Icon name="i-lucide:upload" class="mr-2" />
            Upload
          </template>
        </Button>
      </div>
      <p v-if="error" class="text-sm text-destructive mt-2">
        {{ error }}
      </p>
    </CardContent>
  </Card>
</template>
