import { catalogEntries, type SectionId } from '../data/catalog';

export type { CatalogEntry, CatalogEntryKind, SectionId } from '../data/catalog';

export function getEntriesForSection(section: SectionId) {
  return catalogEntries
    .filter((entry) => entry.sections.includes(section))
    .slice()
    .sort((a, b) => (a.order?.[section] ?? -9999) - (b.order?.[section] ?? -9999));
}

export function getEntryCounts() {
  return catalogEntries.reduce(
    (counts, entry) => {
      counts[entry.kind] += 1;
      return counts;
    },
    { local: 0, external: 0, asset: 0 }
  );
}
