import { catalogEntries, type SectionId } from '../data/catalog';

export type { CatalogEntry, CatalogEntryKind, SectionId } from '../data/catalog';

export function getEntriesForSection(section: SectionId) {
  return catalogEntries
    .map((entry, index) => ({ entry, index }))
    .filter(({ entry }) => entry.sections.includes(section))
    .sort((a, b) => {
      const orderA = a.entry.order?.[section];
      const orderB = b.entry.order?.[section];

      if (orderA !== undefined || orderB !== undefined) {
        return (orderA ?? -9999) - (orderB ?? -9999) || a.index - b.index;
      }

      return a.index - b.index;
    })
    .map(({ entry }) => entry);
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
