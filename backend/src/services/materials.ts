import { Material } from '../types';
import fs from 'fs';
import path from 'path';

export class MaterialsService {
  private materials: Record<string, any>;

  constructor() {
    const materialsPath = path.join(__dirname, '../data/materials.json');
    this.materials = JSON.parse(fs.readFileSync(materialsPath, 'utf-8'));
  }

  getMaterialsBySubject(subject: string): Material[] {
    const subjectMaterials = this.materials[subject];
    if (!subjectMaterials) return [];

    const allMaterials: Material[] = [];
    
    // Flatten the structure into a single array of materials
    for (const category of Object.keys(subjectMaterials)) {
      const materials = subjectMaterials[category];
      allMaterials.push(...materials);
    }

    return allMaterials;
  }

  getMaterialsByDifficulty(subject: string, difficulty: string): Material[] {
    const materials = this.getMaterialsBySubject(subject);
    return materials.filter(material => material.difficulty === difficulty);
  }

  getMaterialsByType(subject: string, type: Material['type']): Material[] {
    const materials = this.getMaterialsBySubject(subject);
    return materials.filter(material => material.type === type);
  }

  searchMaterialsByTags(subject: string, tags: string[]): Material[] {
    const materials = this.getMaterialsBySubject(subject);
    return materials.filter(material =>
      tags.some(tag => material.tags.includes(tag))
    );
  }
}

export const materialsService = new MaterialsService();
