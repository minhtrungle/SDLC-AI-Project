import { ref } from "vue";

const message = ref("");

/** Screen-reader status messages (WCAG 4.1.3) rendered in one aria-live region. */
export function useAnnouncer() {
  return {
    message,
    announce(text: string) {
      message.value = text;
    },
  };
}
